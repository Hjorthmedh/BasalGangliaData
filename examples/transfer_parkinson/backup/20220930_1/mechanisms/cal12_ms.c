/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__cal12_ms
#define _nrn_initial _nrn_initial__cal12_ms
#define nrn_cur _nrn_cur__cal12_ms
#define _nrn_current _nrn_current__cal12_ms
#define nrn_jacob _nrn_jacob__cal12_ms
#define nrn_state _nrn_state__cal12_ms
#define _net_receive _net_receive__cal12_ms 
#define rates rates__cal12_ms 
#define states states__cal12_ms 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define pbar _p[0]
#define pbar_columnindex 0
#define modDA _p[1]
#define modDA_columnindex 1
#define maxModDA _p[2]
#define maxModDA_columnindex 2
#define levelDA _p[3]
#define levelDA_columnindex 3
#define modACh _p[4]
#define modACh_columnindex 4
#define maxModACh _p[5]
#define maxModACh_columnindex 5
#define levelACh _p[6]
#define levelACh_columnindex 6
#define ical _p[7]
#define ical_columnindex 7
#define m _p[8]
#define m_columnindex 8
#define h _p[9]
#define h_columnindex 9
#define ecal _p[10]
#define ecal_columnindex 10
#define cali _p[11]
#define cali_columnindex 11
#define calo _p[12]
#define calo_columnindex 12
#define minf _p[13]
#define minf_columnindex 13
#define mtau _p[14]
#define mtau_columnindex 14
#define hinf _p[15]
#define hinf_columnindex 15
#define htau _p[16]
#define htau_columnindex 16
#define Dm _p[17]
#define Dm_columnindex 17
#define Dh _p[18]
#define Dh_columnindex 18
#define v _p[19]
#define v_columnindex 19
#define _g _p[20]
#define _g_columnindex 20
#define _ion_cali	*_ppvar[0]._pval
#define _ion_calo	*_ppvar[1]._pval
#define _ion_ical	*_ppvar[2]._pval
#define _ion_dicaldv	*_ppvar[3]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_efun(void);
 static void _hoc_ghk(void);
 static void _hoc_modulationACh(void);
 static void _hoc_modulationDA(void);
 static void _hoc_rates(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_cal12_ms", _hoc_setdata,
 "efun_cal12_ms", _hoc_efun,
 "ghk_cal12_ms", _hoc_ghk,
 "modulationACh_cal12_ms", _hoc_modulationACh,
 "modulationDA_cal12_ms", _hoc_modulationDA,
 "rates_cal12_ms", _hoc_rates,
 0, 0
};
#define efun efun_cal12_ms
#define ghk ghk_cal12_ms
#define modulationACh modulationACh_cal12_ms
#define modulationDA modulationDA_cal12_ms
 extern double efun( _threadargsprotocomma_ double );
 extern double ghk( _threadargsprotocomma_ double , double , double );
 extern double modulationACh( _threadargsproto_ );
 extern double modulationDA( _threadargsproto_ );
 /* declare global and static user variables */
#define a a_cal12_ms
 double a = 0.17;
#define q q_cal12_ms
 double q = 2;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "pbar_cal12_ms", "cm/s",
 "ical_cal12_ms", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "a_cal12_ms", &a_cal12_ms,
 "q_cal12_ms", &q_cal12_ms,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(NrnThread*, _Memb_list*, int);
static void nrn_state(NrnThread*, _Memb_list*, int);
 static void nrn_cur(NrnThread*, _Memb_list*, int);
static void  nrn_jacob(NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(NrnThread*, _Memb_list*, int);
static void _ode_matsol(NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[4]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"cal12_ms",
 "pbar_cal12_ms",
 "modDA_cal12_ms",
 "maxModDA_cal12_ms",
 "levelDA_cal12_ms",
 "modACh_cal12_ms",
 "maxModACh_cal12_ms",
 "levelACh_cal12_ms",
 0,
 "ical_cal12_ms",
 0,
 "m_cal12_ms",
 "h_cal12_ms",
 0,
 0};
 static Symbol* _cal_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 21, _prop);
 	/*initialize range parameters*/
 	pbar = 0;
 	modDA = 0;
 	maxModDA = 1;
 	levelDA = 0;
 	modACh = 0;
 	maxModACh = 1;
 	levelACh = 0;
 	_prop->param = _p;
 	_prop->param_size = 21;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_cal_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* cali */
 	_ppvar[1]._pval = &prop_ion->param[2]; /* calo */
 	_ppvar[2]._pval = &prop_ion->param[3]; /* ical */
 	_ppvar[3]._pval = &prop_ion->param[4]; /* _ion_dicaldv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _cal12_ms_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("cal", 2.0);
 	_cal_sym = hoc_lookup("cal_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 21, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "cal_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "cal_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "cal_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cal_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 cal12_ms cal12_ms.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 
#define FARADAY _nrnunit_FARADAY[_nrnunit_use_legacy_]
static double _nrnunit_FARADAY[2] = {0x1.78e555060882cp+16, 96485.3}; /* 96485.3321233100141 */
 
#define R _nrnunit_R[_nrnunit_use_legacy_]
static double _nrnunit_R[2] = {0x1.0a1013e8990bep+3, 8.3145}; /* 8.3144626181532395 */
static int _reset;
static char *modelname = "HVA L-type calcium current (Cav1.2)";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(_threadargsproto_);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   rates ( _threadargs_ ) ;
   Dm = ( minf - m ) / mtau * q ;
   Dh = ( hinf - h ) / htau * q ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 rates ( _threadargs_ ) ;
 Dm = Dm  / (1. - dt*( ( ( ( ( - 1.0 ) ) ) / mtau )*( q ) )) ;
 Dh = Dh  / (1. - dt*( ( ( ( ( - 1.0 ) ) ) / htau )*( q ) )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) { {
   rates ( _threadargs_ ) ;
    m = m + (1. - exp(dt*(( ( ( ( - 1.0 ) ) ) / mtau )*( q ))))*(- ( ( ( ( minf ) ) / mtau )*( q ) ) / ( ( ( ( ( - 1.0 ) ) ) / mtau )*( q ) ) - m) ;
    h = h + (1. - exp(dt*(( ( ( ( - 1.0 ) ) ) / htau )*( q ))))*(- ( ( ( ( hinf ) ) / htau )*( q ) ) / ( ( ( ( ( - 1.0 ) ) ) / htau )*( q ) ) - h) ;
   }
  return 0;
}
 
static int  rates ( _threadargsproto_ ) {
    minf = 1.0 / ( 1.0 + exp ( ( v - ( - 8.9 ) ) / ( - 6.7 ) ) ) ;
   mtau = 0.06 + 1.0 / ( exp ( ( v - 10.0 ) / 20.0 ) + exp ( ( v - ( - 17.0 ) ) / - 48.0 ) ) ;
   hinf = 1.0 / ( 1.0 + exp ( ( v - ( - 13.4 ) ) / 11.9 ) ) ;
   htau = 44.3 ;
     return 0; }
 
static void _hoc_rates(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 rates ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 
double ghk ( _threadargsprotocomma_ double _lv , double _lci , double _lco ) {
   double _lghk;
 double _lz , _leci , _leco ;
 _lz = ( 1e-3 ) * 2.0 * FARADAY * _lv / ( R * ( celsius + 273.15 ) ) ;
   _leco = _lco * efun ( _threadargscomma_ _lz ) ;
   _leci = _lci * efun ( _threadargscomma_ - _lz ) ;
   _lghk = ( 1e-3 ) * 2.0 * FARADAY * ( _leci - _leco ) ;
   
return _lghk;
 }
 
static void _hoc_ghk(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  ghk ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
double efun ( _threadargsprotocomma_ double _lz ) {
   double _lefun;
 if ( fabs ( _lz ) < 1e-4 ) {
     _lefun = 1.0 - _lz / 2.0 ;
     }
   else {
     _lefun = _lz / ( exp ( _lz ) - 1.0 ) ;
     }
   
return _lefun;
 }
 
static void _hoc_efun(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  efun ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double modulationDA ( _threadargsproto_ ) {
   double _lmodulationDA;
 _lmodulationDA = 1.0 + modDA * ( maxModDA - 1.0 ) * levelDA ;
   
return _lmodulationDA;
 }
 
static void _hoc_modulationDA(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  modulationDA ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 
double modulationACh ( _threadargsproto_ ) {
   double _lmodulationACh;
 _lmodulationACh = 1.0 + modACh * ( maxModACh - 1.0 ) * levelACh ;
   
return _lmodulationACh;
 }
 
static void _hoc_modulationACh(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  modulationACh ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cali = _ion_cali;
  calo = _ion_calo;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cali = _ion_cali;
  calo = _ion_calo;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_cal_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_cal_sym, _ppvar, 1, 2);
   nrn_update_ion_pointer(_cal_sym, _ppvar, 2, 3);
   nrn_update_ion_pointer(_cal_sym, _ppvar, 3, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  h = h0;
  m = m0;
 {
   rates ( _threadargs_ ) ;
   m = minf ;
   h = hinf ;
   }
 
}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  cali = _ion_cali;
  calo = _ion_calo;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   ical = pbar * m * ( h * a + 1.0 - a ) * ghk ( _threadargscomma_ v , cali , calo ) * modulationDA ( _threadargs_ ) * modulationACh ( _threadargs_ ) ;
   }
 _current += ical;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  cali = _ion_cali;
  calo = _ion_calo;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dical;
  _dical = ical;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dicaldv += (_dical - ical)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ical += ical ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  cali = _ion_cali;
  calo = _ion_calo;
 {   states(_p, _ppvar, _thread, _nt);
  } }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = m_columnindex;  _dlist1[0] = Dm_columnindex;
 _slist1[1] = h_columnindex;  _dlist1[1] = Dh_columnindex;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "cal12_ms.mod";
static const char* nmodl_file_text = 
  "TITLE HVA L-type calcium current (Cav1.2)\n"
  "\n"
  "COMMENT\n"
  "\n"
  "Neuromodulation is added as functions:\n"
  "    \n"
  "    modulationDA = 1 + modDA*(maxModDA-1)*levelDA\n"
  "\n"
  "where:\n"
  "    \n"
  "    modDA  [0]: is a switch for turning modulation on or off {1/0}\n"
  "    maxModDA [1]: is the maximum modulation for this specific channel (read from the param file)\n"
  "                    e.g. 10% increase would correspond to a factor of 1.1 (100% +10%) {0-inf}\n"
  "    levelDA  [0]: is an additional parameter for scaling modulation. \n"
  "                Can be used simulate non static modulation by gradually changing the value from 0 to 1 {0-1}\n"
  "									\n"
  "	  Further neuromodulators can be added by for example:\n"
  "          modulationDA = 1 + modDA*(maxModDA-1)\n"
  "	  modulationACh = 1 + modACh*(maxModACh-1)\n"
  "	  ....\n"
  "\n"
  "	  etc. for other neuromodulators\n"
  "	  \n"
  "	   \n"
  "								     \n"
  "[] == default values\n"
  "{} == ranges\n"
  "    \n"
  "ENDCOMMENT\n"
  "\n"
  "\n"
  "UNITS {\n"
  "    (mV) = (millivolt)\n"
  "    (mA) = (milliamp)\n"
  "    (S) = (siemens)\n"
  "    (molar) = (1/liter)\n"
  "    (mM) = (millimolar)\n"
  "    FARADAY = (faraday) (coulomb)\n"
  "    R = (k-mole) (joule/degC)\n"
  "}\n"
  "\n"
  "NEURON {\n"
  "    SUFFIX cal12_ms\n"
  "    USEION cal READ cali, calo WRITE ical VALENCE 2\n"
  "    RANGE pbar, ical\n"
  "    RANGE modDA, maxModDA, levelDA\n"
  "    RANGE modACh, maxModACh, levelACh\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "    pbar = 0.0 (cm/s)\n"
  "    a = 0.17\n"
  "    :q = 1	          : room temperature 22-25 C\n"
  "    q = 2	          : body temperature 35 C\n"
  "    modDA = 0\n"
  "    maxModDA = 1\n"
  "    levelDA = 0\n"
  "    modACh = 0\n"
  "    maxModACh = 1 \n"
  "    levelACh = 0\n"
  "		   \n"
  "} \n"
  "\n"
  "ASSIGNED { \n"
  "    v (mV)\n"
  "    ical (mA/cm2)\n"
  "    ecal (mV)\n"
  "    celsius (degC)\n"
  "    cali (mM)\n"
  "    calo (mM)\n"
  "    minf\n"
  "    mtau (ms)\n"
  "    hinf\n"
  "    htau (ms)\n"
  "}\n"
  "\n"
  "STATE { m h }\n"
  "\n"
  "BREAKPOINT {\n"
  "    SOLVE states METHOD cnexp\n"
  "    ical = pbar*m*(h*a+1-a)*ghk(v, cali, calo)*modulationDA()*modulationACh()\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "    rates()\n"
  "    m = minf\n"
  "    h = hinf\n"
  "}\n"
  "\n"
  "DERIVATIVE states { \n"
  "    rates()\n"
  "    m' = (minf-m)/mtau*q\n"
  "    h' = (hinf-h)/htau*q\n"
  "}\n"
  "\n"
  "PROCEDURE rates() {\n"
  "    UNITSOFF\n"
  "    minf = 1/(1+exp((v-(-8.9))/(-6.7)))\n"
  "    mtau = 0.06+1/(exp((v-10)/20)+exp((v-(-17))/-48))\n"
  "    hinf = 1/(1+exp((v-(-13.4))/11.9))\n"
  "    htau = 44.3\n"
  "    UNITSON\n"
  "}\n"
  "\n"
  "FUNCTION ghk(v (mV), ci (mM), co (mM)) (.001 coul/cm3) {\n"
  "    LOCAL z, eci, eco\n"
  "    z = (1e-3)*2*FARADAY*v/(R*(celsius+273.15))\n"
  "    eco = co*efun(z)\n"
  "    eci = ci*efun(-z)\n"
  "    ghk = (1e-3)*2*FARADAY*(eci-eco)\n"
  "}\n"
  "\n"
  "FUNCTION efun(z) {\n"
  "    if (fabs(z) < 1e-4) {\n"
  "        efun = 1-z/2\n"
  "    }else{\n"
  "        efun = z/(exp(z)-1)\n"
  "    }\n"
  "}\n"
  "\n"
  "\n"
  "FUNCTION modulationDA() {\n"
  "    : returns modulation factor\n"
  "    \n"
  "    modulationDA = 1 + modDA*(maxModDA-1)*levelDA \n"
  "}\n"
  "\n"
  "FUNCTION modulationACh() {\n"
  "    : returns modulation factor\n"
  "    \n"
  "    modulationACh = 1 + modACh*(maxModACh-1)*levelACh \n"
  "}\n"
  "\n"
  "\n"
  "COMMENT\n"
  "\n"
  "Activation curve was reconstructed for cultured NAc neurons from P5-P32\n"
  "Charles River rat pups [1].   Activation time constant is from the\n"
  "rodent neuron culture (both rat and mouse cells), room temperature 22-25\n"
  "C [2, Fig.15A]. Inactivation curve of CaL v1.3 current was taken from HEK\n"
  "cells [3, Fig.2 and p.819] at room temperature.\n"
  "\n"
  "Original NEURON model by Wolf (2005) [4] was modified by Alexander Kozlov\n"
  "<akozlov@csc.kth.se>. Kinetics of m1h type was used [5,6]. Activation\n"
  "time constant was refitted to avoid singularity.\n"
  "\n"
  "[1] Churchill D, Macvicar BA (1998) Biophysical and pharmacological\n"
  "characterization of voltage-dependent Ca2+ channels in neurons isolated\n"
  "from rat nucleus accumbens. J Neurophysiol 79(2):635-47.\n"
  "\n"
  "[2] Kasai H, Neher E (1992) Dihydropyridine-sensitive and\n"
  "omega-conotoxin-sensitive calcium channels in a mammalian\n"
  "neuroblastoma-glioma cell line. J Physiol 448:161-88.\n"
  "\n"
  "[3] Bell DC, Butcher AJ, Berrow NS, Page KM, Brust PF, Nesterova A,\n"
  "Stauderman KA, Seabrook GR, Nurnberg B, Dolphin AC (2001) Biophysical\n"
  "properties, pharmacology, and modulation of human, neuronal L-type\n"
  "(alpha(1D), Ca(V)1.3) voltage-dependent calcium currents. J Neurophysiol\n"
  "85:816-827.\n"
  "\n"
  "[4] Wolf JA, Moyer JT, Lazarewicz MT, Contreras D, Benoit-Marand M,\n"
  "O'Donnell P, Finkel LH (2005) NMDA/AMPA ratio impacts state transitions\n"
  "and entrainment to oscillations in a computational model of the nucleus\n"
  "accumbens medium spiny projection neuron. J Neurosci 25(40):9080-95.\n"
  "\n"
  "[5] Evans RC, Morera-Herreras T, Cui Y, Du K, Sheehan T, Kotaleski JH,\n"
  "Venance L, Blackwell KT (2012) The effects of NMDA subunit composition on\n"
  "calcium influx and spike timing-dependent plasticity in striatal medium\n"
  "spiny neurons. PLoS Comput Biol 8(4):e1002493.\n"
  "\n"
  "[6] Tuckwell HC (2012) Quantitative aspects of L-type Ca2+ currents. Prog\n"
  "Neurobiol 96(1):1-31.\n"
  "\n"
  "add justification for modulation\n"
  "\n"
  "ENDCOMMENT\n"
  ;
#endif
