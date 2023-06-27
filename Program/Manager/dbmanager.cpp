#include "dbmanager.h"

DbManager::DbManager(const char* driver, const char* path)
{
    db = QSqlDatabase::addDatabase(driver);
    db.setDatabaseName(path);
}

std::vector<Model> DbManager::GetInfo(const char* query)
{
    std::vector<Model> info;
    QSqlQuery DbQuery(db);
    if (DbQuery.exec(query))
    {
        QSqlRecord rec = DbQuery.record();
        while(DbQuery.next())
        {
            info.push_back(Model(
                                 DbQuery.value(rec.indexOf("productId")),
                                 DbQuery.value(rec.indexOf("name")),
                                 DbQuery.value(rec.indexOf("basePrice")),
                                 DbQuery.value(rec.indexOf("salePrice")),
                                 DbQuery.value(rec.indexOf("bonusRubles")),
                                 DbQuery.value(rec.indexOf("linkToproduct"))
                                 )
                           );
        }
    }
    return info;
}

Model DbManager::GetItem(const char* query)
{
    QSqlQuery DbQuery(db);
    Model *item;
    if (DbQuery.exec(query))
    {
        QSqlRecord rec = DbQuery.record();
        while(DbQuery.next())
        {
             item = new Model(
                DbQuery.value(rec.indexOf("productId")),
                DbQuery.value(rec.indexOf("name")),
                DbQuery.value(rec.indexOf("basePrice")),
                DbQuery.value(rec.indexOf("salePrice")),
                DbQuery.value(rec.indexOf("bonusRubles")),
                DbQuery.value(rec.indexOf("linkToproduct"))
                );
        }

        if (DbQuery.exec(QString("SELECT pathImage FROM Images WHERE productId=\"" + QString::number(item->GetProductId()) + "\"").toStdString().c_str()))
        {
            rec = DbQuery.record();
            std::vector <QString> tmp;
            while(DbQuery.next())
            {
                tmp.push_back(DbQuery.value(rec.indexOf("pathImage")).toString());
            }
            item->SetPathToImage(tmp);
            tmp.clear();
        }

        return *item;
    }
    return Model();
}

bool DbManager::Open()
{
    return db.open();
}


bool DbManager::Close()
{
    db.close();
    if (!db.isOpen())
        return true;
    return false;
}
