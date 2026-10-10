// Checkpoint / restart for PF-FDTD CW runs.
//
// Dumps the full dynamic solver state (fields, plasma moments, retarded-ABC
// history, time level indices) to <fileout>.ckpt so an interrupted run can
// resume bit-identically instead of restarting from t=0. Static setup data
// (grid, PEC flags, sheath mask, ambient density) is rebuilt by the normal
// init path on resume and only the dynamic arrays are overwritten.
//
// Usage (pffdtd.cpp): pass argv[16] = checkpoint interval in steps (0 = off).
// The solver writes <fileout>.ckpt.tmp then renames atomically every interval,
// resumes automatically when <fileout>.ckpt exists, and deletes it on clean
// completion. The .vc record is appended on resume, not rewritten.
#pragma once

// Descriptor for one retarded-ABC history array (darray4 layout).
struct BCArray {
  double**** a;
  int x1, x2, y1, y2, z1, z2, m1, m2;
};

int ckpt_exists(const char* path);
// Returns 0 on success.
int ckpt_write(const char* path, int iter, double timev, int ip,
               const BCArray* bcs, int nbcs);
// Returns 0 on success and fills iter/timev/ip; verifies grid + run tag.
int ckpt_read(const char* path, int* iter, double* timev, int* ip,
              const BCArray* bcs, int nbcs);
// Truncate a sampled record (<fileout><suffix>) back to the checkpoint
// iteration so samples written between the last checkpoint and the
// interruption are not duplicated on resume. The record holds a header
// line plus one line per sample, sample k <-> iteration 1+k*rate.
// Returns 0 on success.
int ckpt_truncate_record(const char* fileout, const char* suffix, int iter,
                         int rate);
