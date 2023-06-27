#include "model.h"

Model::Model(QVariant productId, QVariant name, QVariant basePrice, QVariant salePrice, QVariant bonusRubls, QVariant linkProduct)
{
    this->productId = productId;
    this->name = name;
    this->basePrice = basePrice;
    this->salePrice = salePrice;
    this->bonusRubls = bonusRubls;
    this->linkProduct = linkProduct;
}

Model::Model()
{
    this->productId = NULL;
    this->name = NULL;
    this->basePrice = NULL;
    this->salePrice = NULL;
    this->bonusRubls = NULL;
    this->linkProduct = NULL;
}

qlonglong Model::GetProductId()
{
    return productId.toLongLong();
}

QString Model::GetName()
{
    return name.toString();
}

qlonglong Model::GetBasePrice()
{
    return basePrice.toLongLong();
}

qlonglong Model::GetSalePrice()
{
    return salePrice.toLongLong();
}

qlonglong Model::GetBonusRubls()
{
    return bonusRubls.toLongLong();
}

QString Model::GetLinkProduct()
{
    return linkProduct.toString();
}

std::vector <QString> Model::GetPathToImage()
{
    return pathToImage;
}

void Model::SetPathToImage(std::vector <QString> pathToImage)
{
    this->pathToImage = pathToImage;
}

Model::~Model()
{
    this->productId = NULL;
    this->name = NULL;
    this->basePrice = NULL;
    this->salePrice = NULL;
    this->bonusRubls = NULL;
    this->linkProduct = NULL;
    this->pathToImage.cend();
}
