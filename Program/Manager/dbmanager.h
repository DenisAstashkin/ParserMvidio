#ifndef DBMANAGER_H
#define DBMANAGER_H

#include <QtSql/QSqlDatabase>
#include <QtSql/QSqlQuery>
#include <QtSql/QSqlRecord>
#include "./model.h"

class DbManager
{
private:
    QSqlDatabase db;
    std::vector <QString> images;
public:
    DbManager();
    DbManager(const char* driver, const char* path);
    Model GetItem(const char* query);
    std::vector<Model> GetInfo(const char* query);
    bool Open();
    bool Close();
};

#endif // DBMANAGER_H
