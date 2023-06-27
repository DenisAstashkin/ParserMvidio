#ifndef MODEL_H
#define MODEL_H

#include <QVariant>

class Model
{
private:
    QVariant productId;
    QVariant name;
    QVariant basePrice;
    QVariant salePrice;
    QVariant bonusRubls;
    QVariant linkProduct;
    std::vector <QString> pathToImage;

public:
    Model();
    Model(QVariant productId, QVariant name, QVariant basePrice, QVariant salePrice, QVariant bonusRubls, QVariant linkProduct);
    qlonglong GetProductId();
    QString GetName();
    qlonglong GetBasePrice();
    qlonglong GetSalePrice();
    qlonglong GetBonusRubls();
    QString GetLinkProduct();
    std::vector <QString> GetPathToImage();
    void SetPathToImage(std::vector <QString> pathToImage);
    ~Model();
};


#endif // MODEL_H
