/********************************************************************************
** Form generated from reading UI file 'qtcalibatorgui.ui'
**
** Created by: Qt User Interface Compiler version 4.8.7
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_QTCALIBATORGUI_H
#define UI_QTCALIBATORGUI_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QDialogButtonBox>
#include <QtGui/QHeaderView>
#include <QtGui/QMainWindow>
#include <QtGui/QMenuBar>
#include <QtGui/QStatusBar>
#include <QtGui/QToolBar>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_QtCalibatorGUI
{
public:
    QWidget *centralWidget;
    QDialogButtonBox *buttonBox;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;
    QToolBar *toolBar;

    void setupUi(QMainWindow *QtCalibatorGUI)
    {
        if (QtCalibatorGUI->objectName().isEmpty())
            QtCalibatorGUI->setObjectName(QString::fromUtf8("QtCalibatorGUI"));
        QtCalibatorGUI->resize(724, 507);
        centralWidget = new QWidget(QtCalibatorGUI);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        buttonBox = new QDialogButtonBox(centralWidget);
        buttonBox->setObjectName(QString::fromUtf8("buttonBox"));
        buttonBox->setGeometry(QRect(190, 190, 166, 25));
        buttonBox->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);
        QtCalibatorGUI->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(QtCalibatorGUI);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 724, 22));
        QtCalibatorGUI->setMenuBar(menuBar);
        mainToolBar = new QToolBar(QtCalibatorGUI);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        QtCalibatorGUI->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(QtCalibatorGUI);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        QtCalibatorGUI->setStatusBar(statusBar);
        toolBar = new QToolBar(QtCalibatorGUI);
        toolBar->setObjectName(QString::fromUtf8("toolBar"));
        QtCalibatorGUI->addToolBar(Qt::TopToolBarArea, toolBar);

        retranslateUi(QtCalibatorGUI);

        QMetaObject::connectSlotsByName(QtCalibatorGUI);
    } // setupUi

    void retranslateUi(QMainWindow *QtCalibatorGUI)
    {
        QtCalibatorGUI->setWindowTitle(QApplication::translate("QtCalibatorGUI", "QtCalibatorGUI", 0, QApplication::UnicodeUTF8));
        toolBar->setWindowTitle(QApplication::translate("QtCalibatorGUI", "toolBar", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class QtCalibatorGUI: public Ui_QtCalibatorGUI {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_QTCALIBATORGUI_H
