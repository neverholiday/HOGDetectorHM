#include "qtcalibatorgui.h"
#include "ui_qtcalibatorgui.h"

QtCalibatorGUI::QtCalibatorGUI(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::QtCalibatorGUI)
{
    ui->setupUi(this);
}

QtCalibatorGUI::~QtCalibatorGUI()
{
    delete ui;
}
