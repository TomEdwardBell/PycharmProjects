#include <Python.h>
#include <QtGlobal>


extern "C" PyObject *PyInit_Qt(void);
extern "C" PyObject *PyInit_QtCore(void);
extern "C" PyObject *PyInit_QtGui(void);
extern "C" PyObject *PyInit_QtWidgets(void);
extern "C" PyObject *PyInit_sip(void);

static struct _inittab extension_modules[] = {
    {"PyQt5.Qt", PyInit_Qt},
    {"PyQt5.QtCore", PyInit_QtCore},
    {"PyQt5.QtGui", PyInit_QtGui},
    {"PyQt5.QtWidgets", PyInit_QtWidgets},
    {"sip", PyInit_sip},
    {NULL, NULL}
};


#include <windows.h>

extern int pyqtdeploy_start(int argc, wchar_t **w_argv,
        struct _inittab *extension_modules, const char *main_module,
        const char *entry_point, const char **path_dirs);

int main(int argc, char **)
{
    LPWSTR *w_argv = CommandLineToArgvW(GetCommandLineW(), &argc);

    return pyqtdeploy_start(argc, w_argv, extension_modules, "__main__", NULL, NULL);
}
