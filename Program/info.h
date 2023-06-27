#ifndef INFO_H
#define INFO_H

#include <QWidget>
#include <QPixmap>
#include "Model/model.h"

namespace Ui {
class Info;
}

class Info : public QWidget
{
    Q_OBJECT

public:
    explicit Info(QWidget *parent = nullptr);

    void SetBasePrice(qlonglong baseprice);
    void SetSalePrice(qlonglong saleprice);
    void SetBonusRubles(qlonglong bonusrubles);
    void SetLink(QString link);
    void SetImage(QString path);

    ~Info();

public slots:
    void SetInfo(Model *item);


private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::Info *ui;
    int count;
    std::vector <QString> Images;
};

#endif // INFO_H
