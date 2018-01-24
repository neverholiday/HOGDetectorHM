#ifndef QTCALIBATORGUI_H
#define QTCALIBATORGUI_H

#include <QMainWindow>

namespace Ui {
class QtCalibatorGUI;
}

class QtCalibatorGUI : public QMainWindow
{
    Q_OBJECT

public:
    explicit QtCalibatorGUI(QWidget *parent = 0);
    ~QtCalibatorGUI();

private:
    Ui::QtCalibatorGUI *ui;
};

#endif // QTCALIBATORGUI_H
