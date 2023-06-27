#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QListWidgetItem>
#include "Manager/dbmanager.h"
#include "Model/model.h"
#include "info.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT
private:
    std::vector<Model> InfoAboutItems;
public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();



private slots:
    void on_ListItems_itemClicked(QListWidgetItem *item);

signals:
    void SendInfo(Model *item);

private:
    Ui::MainWindow *ui;
    DbManager *manager;

};
#endif // MAINWINDOW_H
