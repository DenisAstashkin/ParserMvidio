#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    manager = new DbManager("QSQLITE", "../Items.db");
    manager->Open();
    InfoAboutItems = manager->GetInfo("SELECT * FROM ItemsMV");
    manager->Close();
    for (Model item : InfoAboutItems)
    {
        ui->ListItems->addItem(item.GetName());
    }
    QObject::connect(this, &MainWindow::SendInfo, ui->widget, &Info::SetInfo);
    ui->ListItems->setCurrentItem(ui->ListItems->item(0));
    this->on_ListItems_itemClicked(ui->ListItems->item(0));
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_ListItems_itemClicked(QListWidgetItem *item)
{
    manager->Open();
    Model Item = manager->GetItem(QString("SELECT * FROM ItemsMV WHERE name=\"" + item->text() + "\"").toStdString().c_str());
    manager->Close();
    emit SendInfo(&Item);
}
