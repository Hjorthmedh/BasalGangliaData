#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _bk_ms_reg(void);
extern void _cadyn_ms_reg(void);
extern void _cal12_ms_reg(void);
extern void _cal13_ms_reg(void);
extern void _caldyn_ms_reg(void);
extern void _can_ms_reg(void);
extern void _caq_ms_reg(void);
extern void _car_ms_reg(void);
extern void _cat32_ms_reg(void);
extern void _cat33_ms_reg(void);
extern void _Im_ms_reg(void);
extern void _kaf_ms_reg(void);
extern void _kas_ms_reg(void);
extern void _kdr_ms_reg(void);
extern void _kir_ms_reg(void);
extern void _naf_ms_reg(void);
extern void _sk_ms_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"bk_ms.mod\"");
    fprintf(stderr, " \"cadyn_ms.mod\"");
    fprintf(stderr, " \"cal12_ms.mod\"");
    fprintf(stderr, " \"cal13_ms.mod\"");
    fprintf(stderr, " \"caldyn_ms.mod\"");
    fprintf(stderr, " \"can_ms.mod\"");
    fprintf(stderr, " \"caq_ms.mod\"");
    fprintf(stderr, " \"car_ms.mod\"");
    fprintf(stderr, " \"cat32_ms.mod\"");
    fprintf(stderr, " \"cat33_ms.mod\"");
    fprintf(stderr, " \"Im_ms.mod\"");
    fprintf(stderr, " \"kaf_ms.mod\"");
    fprintf(stderr, " \"kas_ms.mod\"");
    fprintf(stderr, " \"kdr_ms.mod\"");
    fprintf(stderr, " \"kir_ms.mod\"");
    fprintf(stderr, " \"naf_ms.mod\"");
    fprintf(stderr, " \"sk_ms.mod\"");
    fprintf(stderr, "\n");
  }
  _bk_ms_reg();
  _cadyn_ms_reg();
  _cal12_ms_reg();
  _cal13_ms_reg();
  _caldyn_ms_reg();
  _can_ms_reg();
  _caq_ms_reg();
  _car_ms_reg();
  _cat32_ms_reg();
  _cat33_ms_reg();
  _Im_ms_reg();
  _kaf_ms_reg();
  _kas_ms_reg();
  _kdr_ms_reg();
  _kir_ms_reg();
  _naf_ms_reg();
  _sk_ms_reg();
}

#if defined(__cplusplus)
}
#endif
