#include "mainwindow.h"
#include <QApplication>
#include <QMessageBox>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    if (std::system("python ../Parser/parser.py") == 1)
        exit(1);
    MainWindow w;
    w.show();
    return a.exec();
}
