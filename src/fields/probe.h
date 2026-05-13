// Lightweight probe API for point probes
#ifndef PROBE_H
#define PROBE_H

// Probe types
#define PROBE_POINT 1

// Initialize probe subsystem. Call after arrays are allocated.
void init_probes();

// Register a simple point probe at grid cell (x,y,z).
// Returns probe id (>=0) or -1 on error.
int register_point_probe(int x, int y, int z, int sample_stride, const char *outfile);

// Sample all probes at current time step (called from main loop)
void probe_sample_all(int iteration, double timev);

// Close probes and flush files (call before exit)
void close_probes();

#endif // PROBE_H
