// Simple probe implementation - point probes only (CSV output)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "probe.h"

// Access fields from main program (externs defined in pffdtd.cpp)
extern double *EX, *EY, *EZ;
extern double *BX, *BY, *BZ;
extern int sx, sy, sz;

typedef struct {
    int used;
    int id;
    int x, y, z;
    int stride; // sample every `stride` iterations
    int counter;
    FILE *fp;
    char fname[256];
} ProbeRec;

static ProbeRec *probes = NULL;
static int max_probes = 0;

// Simple flat index helper for field arrays (assumes existing IDX macros in codebase)
static int idx_cell(int x, int y, int z)
{
    // bounds check
    if (x < 0) x = 0; if (y < 0) y = 0; if (z < 0) z = 0;
    if (x > sx) x = sx; if (y > sy) y = sy; if (z > sz) z = sz;
    return (x*(sy+1)*(sz+1) + y*(sz+1) + z);
}

void init_probes()
{
    max_probes = 64;
    probes = (ProbeRec*)calloc(max_probes, sizeof(ProbeRec));
    for (int i=0;i<max_probes;i++) probes[i].used = 0;
}

int register_point_probe(int x, int y, int z, int sample_stride, const char *outfile)
{
    if (!probes) init_probes();
    int id = -1;
    for (int i=0;i<max_probes;i++) {
        if (!probes[i].used) { id = i; break; }
    }
    if (id < 0) return -1;
    probes[id].used = 1;
    probes[id].id = id;
    probes[id].x = x;
    probes[id].y = y;
    probes[id].z = z;
    probes[id].stride = (sample_stride>0)?sample_stride:1;
    probes[id].counter = 0;
    if (outfile) strncpy(probes[id].fname, outfile, sizeof(probes[id].fname)-1);
    else snprintf(probes[id].fname, sizeof(probes[id].fname), "results/probes/probe_%d.csv", id);
    // open file (append)
    probes[id].fp = fopen(probes[id].fname, "w");
    if (probes[id].fp) {
        fprintf(probes[id].fp, "time,Ex,Ey,Ez,Bx,By,Bz\n");
        fflush(probes[id].fp);
    }
    return id;
}

void probe_sample_all(int iteration, double timev)
{
    if (!probes) return;
    for (int i=0;i<max_probes;i++) {
        if (!probes[i].used) continue;
        probes[i].counter++;
        if ((probes[i].counter % probes[i].stride) != 0) continue;
        // sample fields at probe location
        int ix = probes[i].x;
        int iy = probes[i].y;
        int iz = probes[i].z;
        int idx = idx_cell(ix,iy,iz);
        double ex=0, ey=0, ez=0, bx=0, by=0, bz=0;
        if (EX) ex = EX[idx];
        if (EY) ey = EY[idx];
        if (EZ) ez = EZ[idx];
        if (BX) bx = BX[idx];
        if (BY) by = BY[idx];
        if (BZ) bz = BZ[idx];
        if (probes[i].fp) {
            fprintf(probes[i].fp, "%e,%e,%e,%e,%e,%e,%e\n", timev, ex, ey, ez, bx, by, bz);
        }
    }
}

void close_probes()
{
    if (!probes) return;
    for (int i=0;i<max_probes;i++) {
        if (probes[i].used && probes[i].fp) fclose(probes[i].fp);
    }
    free(probes);
    probes = NULL;
    max_probes = 0;
}
