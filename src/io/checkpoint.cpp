// Checkpoint / restart for PF-FDTD CW runs. See checkpoint.h.
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include "checkpoint.h"
#include "../physics/plasma.h"

namespace {

const char kMagic[8] = {'P', 'F', 'F', 'D', 'C', 'K', 'P', 'T'};
const int kVersion = 1;

long nfield() { return (long)(sx + 1) * (sy + 1) * (sz + 1); }

struct Counts {
  long f2;   // E/B arrays: nfield*2 + 1  (darray1(0, nfield*2))
  long f1;   // ER arrays:  nfield + 1
  long p5;   // U/N arrays: nfield*3*NS + 1
  long pn0;  // N0_SPATIAL: nfield*NS + 1
};

Counts counts() {
  Counts c;
  long nf = nfield();
  c.f2 = nf * 2 + 1;
  c.f1 = nf + 1;
  c.p5 = nf * 3 * NS + 1;
  c.pn0 = nf * NS + 1;
  return c;
}

bool wr(FILE* f, const void* p, size_t n) {
  return fwrite(p, 1, n, f) == n;
}
bool rd(FILE* f, void* p, size_t n) {
  return fread(p, 1, n, f) == n;
}
bool wr64(FILE* f, long v) { return wr(f, &v, sizeof(v)); }
bool rd64(FILE* f, long* v) { return rd(f, v, sizeof(*v)); }
bool wri(FILE* f, int v) { return wr(f, &v, sizeof(v)); }
bool rdi(FILE* f, int* v) { return rd(f, v, sizeof(*v)); }
bool wrd(FILE* f, double v) { return wr(f, &v, sizeof(v)); }
bool rdd(FILE* f, double* v) { return rd(f, v, sizeof(*v)); }

bool wr_bc(FILE* f, const BCArray& b) {
  long n = (long)(b.x2 - b.x1 + 1) * (b.y2 - b.y1 + 1) * (b.z2 - b.z1 + 1) *
           (b.m2 - b.m1 + 1);
  // darray4 stores data contiguously starting at a[x1][y1][z1] (= [...][m1]).
  return wr(f, b.a[b.x1][b.y1][b.z1], (size_t)n * sizeof(double));
}
bool rd_bc(FILE* f, const BCArray& b) {
  long n = (long)(b.x2 - b.x1 + 1) * (b.y2 - b.y1 + 1) * (b.z2 - b.z1 + 1) *
           (b.m2 - b.m1 + 1);
  return rd(f, b.a[b.x1][b.y1][b.z1], (size_t)n * sizeof(double));
}

bool write_header(FILE* f, int iter, double timev, int ip) {
  int pflag = (UX != nullptr) ? 1 : 0;
  return wr(f, kMagic, 8) && wri(f, kVersion) && wri(f, sx) && wri(f, sy) &&
         wri(f, sz) && wri(f, NS) && wri(f, Sd) && wrd(f, FREQ_PLASMA) &&
         wrd(f, dt) && wri(f, pflag) && wri(f, iter) && wrd(f, timev) &&
         wri(f, ip);
}

bool read_header(FILE* f, int* iter, double* timev, int* ip) {
  char magic[8];
  int ver, gx, gy, gz, gns, gsd, gpflag;
  double gfp, gdt;
  if (!rd(f, magic, 8) || memcmp(magic, kMagic, 8) != 0) return false;
  if (!rdi(f, &ver) || ver != kVersion) return false;
  if (!rdi(f, &gx) || !rdi(f, &gy) || !rdi(f, &gz) || !rdi(f, &gns)) return false;
  if (!rdi(f, &gsd) || !rdd(f, &gfp) || !rdd(f, &gdt)) return false;
  if (!rdi(f, &gpflag)) return false;
  if (gx != sx || gy != sy || gz != sz || gns != NS) return false;
  if (gsd != Sd || gfp != FREQ_PLASMA || gdt != dt) return false;
  if (gpflag != ((UX != nullptr) ? 1 : 0)) return false;
  return rdi(f, iter) && rdd(f, timev) && rdi(f, ip);
}

}  // namespace

int ckpt_exists(const char* path) {
  FILE* f = fopen(path, "rb");
  if (!f) return 0;
  fclose(f);
  return 1;
}

int ckpt_write(const char* path, int iter, double timev, int ip,
               const BCArray* bcs, int nbcs) {
  Counts c = counts();
  char tmp[600];
  snprintf(tmp, sizeof(tmp), "%s.tmp", path);
  FILE* f = fopen(tmp, "wb");
  if (!f) return 1;
  bool ok = write_header(f, iter, timev, ip);
  // EM fields (both time levels) + PEC flags
  double* ef[6] = {EX, EY, EZ, BX, BY, BZ};
  for (int k = 0; k < 6 && ok; k++) ok = wr(f, ef[k], (size_t)c.f2 * 8);
  double* erf[3] = {ERX, ERY, ERZ};
  for (int k = 0; k < 3 && ok; k++) ok = wr(f, erf[k], (size_t)c.f1 * 8);
  // Plasma moments (all time levels/species) + ambient/coupling fields.
  // Skipped entirely when plasma is off (arrays null); header pflag covers it.
  if (UX != nullptr) {
    double* pf[4] = {UX, UY, UZ, N};
    for (int k = 0; k < 4 && ok; k++) ok = wr(f, pf[k], (size_t)c.p5 * 8);
    if (ok) ok = wr(f, N0_SPATIAL, (size_t)c.pn0 * 8);
    if (ok) ok = wr(f, SIG, (size_t)c.f1 * 8);
    if (ok) ok = wr(f, QF, (size_t)c.f1 * 8);
  }
  // Retarded-ABC history
  for (int k = 0; k < nbcs && ok; k++) ok = wr_bc(f, bcs[k]);
  // Trailer: iteration again so a torn write is detectable
  if (ok) ok = wri(f, iter);
  fclose(f);
  if (!ok) {
    remove(tmp);
    return 2;
  }
  if (rename(tmp, path) != 0) {
    remove(tmp);
    return 3;
  }
  return 0;
}

int ckpt_truncate_record(const char* fileout, const char* suffix, int iter,
                         int rate) {
  if (rate < 1) rate = 1;
  // The checkpoint is written after the loop increments, so (iter, timev)
  // is the start of the next iteration; the last fully processed iteration
  // is iter-1. Sample k was taken at loop-top iteration 1+k*rate, so keep
  // samples with 1+k*rate <= iter-1.
  long nkeep = iter >= 2 ? (iter - 2) / rate + 1 : 0;
  char path[600], tmp[620];
  snprintf(path, sizeof(path), "%s%s", fileout, suffix);
  snprintf(tmp, sizeof(tmp), "%s.trunc", path);
  FILE* f = fopen(path, "r");
  if (!f) return 1;
  FILE* o = fopen(tmp, "w");
  if (!o) {
    fclose(f);
    return 1;
  }
  char* line = nullptr;
  size_t cap = 0;
  ssize_t len;
  long n = 0;  // lines written; line 0 is the header
  bool ok = true;
  while ((len = getline(&line, &cap, f)) != -1) {
    if (n == 0 || n <= nkeep) {
      if (fwrite(line, 1, (size_t)len, o) != (size_t)len) {
        ok = false;
        break;
      }
    }
    n++;
  }
  free(line);
  fclose(f);
  fclose(o);
  if (!ok) {
    remove(tmp);
    return 2;
  }
  if (rename(tmp, path) != 0) {
    remove(tmp);
    return 3;
  }
  return 0;
}

int ckpt_read(const char* path, int* iter, double* timev, int* ip,
              const BCArray* bcs, int nbcs) {
  Counts c = counts();
  FILE* f = fopen(path, "rb");
  if (!f) return 1;
  bool ok = read_header(f, iter, timev, ip);
  double* ef[6] = {EX, EY, EZ, BX, BY, BZ};
  for (int k = 0; k < 6 && ok; k++) ok = rd(f, ef[k], (size_t)c.f2 * 8);
  double* erf[3] = {ERX, ERY, ERZ};
  for (int k = 0; k < 3 && ok; k++) ok = rd(f, erf[k], (size_t)c.f1 * 8);
  // Plasma arrays exist only when plasma==1 (header pflag verified above).
  if (UX != nullptr) {
    double* pf[4] = {UX, UY, UZ, N};
    for (int k = 0; k < 4 && ok; k++) ok = rd(f, pf[k], (size_t)c.p5 * 8);
    if (ok) ok = rd(f, N0_SPATIAL, (size_t)c.pn0 * 8);
    if (ok) ok = rd(f, SIG, (size_t)c.f1 * 8);
    if (ok) ok = rd(f, QF, (size_t)c.f1 * 8);
  }
  for (int k = 0; k < nbcs && ok; k++) ok = rd_bc(f, bcs[k]);
  int trailer = -1;
  if (ok) ok = rdi(f, &trailer) && trailer == *iter;
  fclose(f);
  return ok ? 0 : 2;
}
