#include "info.h"
#include "ui_info.h"

Info::Info(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Info)
{
    ui->setupUi(this);
}

void Info::SetBasePrice(qlonglong baseprice)
{
    ui->BasePrice->setText(QString::number(baseprice) + " рублей");
}

void Info::SetSalePrice(qlonglong saleprice)
{
    ui->SalePrice->setText(QString::number(saleprice) + " рублей");
}

void Info::SetBonusRubles(qlonglong bonusrubles)
{
    ui->BonusRubles->setText(QString::number(bonusrubles) + " бонусов");
}

void Info::SetLink(QString link)
{
    ui->Link->setText(link);
}

void Info::SetImage(QString path)
{
    QPixmap pix(path);
    ui->Image->setPixmap(pix.scaled(ui->Image->width(),
                                    ui->Image->height(),
                                    Qt::KeepAspectRatio));
}

void Info::SetInfo(Model *item)
{
    count = 0;
    this->Images.clear();
    ui->BasePrice->setText(QString::number(item->GetBasePrice()));
    ui->SalePrice->setText(QString::number(item->GetSalePrice()));
    ui->BonusRubles->setText(QString::number(item->GetBonusRubls()));
    ui->Link->setText(item->GetLinkProduct());
    ui->BasePrice->setText(QString::number(item->GetBasePrice()));
    this->Images = item->GetPathToImage();
    if (!Images.empty())
        this->SetImage(this->Images[count]);

    item = nullptr;
}

Info::~Info()
{
    delete ui;
}

void Info::on_pushButton_clicked()
{
    if (Images.empty())
        return;

    if (count + 1 < Images.size())
        count++;
    else
        count = 0;
    this->SetImage(Images[count]);
}


void Info::on_pushButton_2_clicked()
{
    if (Images.empty())
        return;

    if (count - 1 < Images.size() && count - 1 >= 0)
        count--;
    else
        count = Images.size() - 1;
    this->SetImage(Images[count]);
}
