# Generated for win-64 and Python v3.7.1.

TEMPLATE = app

QT += widgets
CONFIG += warn_off

RESOURCES = \
    resources/pyqtdeploy.qrc

DEFINES += PYQTDEPLOY_FROZEN_MAIN PYQTDEPLOY_OPTIMIZED

INCLUDEPATH += C:/Users/Tom/AppData/Local/Programs/Python/Python37/include

SOURCES = pyqtdeploy_main.cpp pyqtdeploy_start.cpp pdytools_module.cpp

HEADERS = pyqtdeploy_version.h frozen_bootstrap.h frozen_bootstrap_external.h frozen_main.h

LIBS += -LC:/Users/Tom/AppData/Local/Programs/Python/Python37/Lib/site-packages
LIBS += -LC:/Users/Tom/AppData/Local/Programs/Python/Python37/Lib/site-packages/PyQt5
LIBS += -LC:/Users/Tom/AppData/Local/Programs/Python/Python37/libs
LIBS += -lQt
LIBS += -lQtCore
LIBS += -lQtGui
LIBS += -lQtWidgets
LIBS += -lpython37
LIBS += -lsip

cython.name = Cython compiler
cython.input = CYTHONSOURCES
cython.output = ${QMAKE_FILE_BASE}.c
cython.variable_out = GENERATED_SOURCES
cython.commands = cython ${QMAKE_FILE_IN} -o ${QMAKE_FILE_OUT}

QMAKE_EXTRA_COMPILERS += cython

linux-* {
    LIBS += -lutil -ldl
}

win32 {
    masm.input = MASMSOURCES
    masm.output = ${QMAKE_FILE_BASE}.obj

    contains(QMAKE_TARGET.arch, x86_64) {
        masm.name = MASM64 compiler
        masm.commands = ml64 /Fo ${QMAKE_FILE_OUT} /c ${QMAKE_FILE_IN}
    } else {
        masm.name = MASM compiler
        masm.commands = ml /Fo ${QMAKE_FILE_OUT} /c ${QMAKE_FILE_IN}
    }

    QMAKE_EXTRA_COMPILERS += masm

    LIBS += -lshlwapi -ladvapi32 -lshell32 -luser32 -lws2_32 -lole32 -loleaut32 -lversion
    DEFINES += MS_WINDOWS _WIN32_WINNT=Py_WINVER NTDDI_VERSION=Py_NTDDI WINVER=Py_WINVER

    # This is added from the qmake spec files but clashes with _pickle.c.
    DEFINES -= UNICODE
}

macx {
    LIBS += -framework SystemConfiguration -framework CoreFoundation
}
