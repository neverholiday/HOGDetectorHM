#include "qtcalibatorgui.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QtCalibatorGUI w;
    w.show();

    return a.exec();
}
