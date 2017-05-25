#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Rado Pitonak <rpitonak@redhat.com>
#

from avocado import main
from avocado.core import exceptions
from moduleframework import module_framework
import time


class DBCheck(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    MONGO_CMD = 'mongo "$MONGODB_DATABASE" -u "$MONGODB_USER" -p "$MONGODB_PASSWORD"'

    # authentication options for admin user
    # https://docs.mongodb.com/manual/reference/program/mongo/#mongo-shell-authentication-options
    MONGO_ADMIN_CMD = 'mongo "$MONGODB_DATABASE" -u "admin" -p "$MONGODB_ADMIN_PASSWORD" --authenticationDatabase admin --authenticationMechanism SCRAM-SHA-1'

    def testConnectToDB(self):
        """
        Test connection to database
        """

        query = "db.getSiblingDB('test_database');"

        self.start()
        time.sleep(3)

        self.run('{} --eval "{}"'.format(self.MONGO_CMD, query))

    def testUserPrivileges(self):
        """
        Testing user privileges. 
        """

        self.start()
        time.sleep(3)

        # mongo db queries stored in dictionary, written in order which they are called
        queries = {"insert1": "db.testData.insert({ y : 1 });",
                   "insert2": "db.testData.insert({ z : 2 });",
                   "print_json": "db.testData.find().forEach(printjson);",
                   "count": "db.testData.count();",
                   "data_drop": "db.testData.drop();",
                   "db_drop": "db.dropDatabase();"}

        self.run('{} --eval "{}"'.format(self.MONGO_CMD, queries["insert1"]))
        self.run('{} --eval "{}"'.format(self.MONGO_CMD, queries["insert2"]))
        self.run('{} --eval "{}"'.format(self.MONGO_CMD, queries["print_json"]))
        self.run('{} --eval "{}"'.format(self.MONGO_CMD, queries["count"]))
        self.run('{} --eval "{}"'.format(self.MONGO_CMD, queries["data_drop"]))
        self.run('{} --eval "{}"'.format(self.MONGO_CMD, queries["db_drop"]))

    def testAdminPrivileges(self):
        """
        Testing privileges for admin user 
        """
        self.start()
        time.sleep(3)

        # mongo db queries stored in dictionary, written in order which they are called
        queries = {"dropUser": "db=db.getSiblingDB('${MONGODB_DATABASE}');db.dropUser('${MONGODB_USER}');",
                   "createUser1": "db=db.getSiblingDB('${MONGODB_DATABASE}'); db.createUser({user:'${MONGODB_USER}',pwd:'${MONGODB_PASSWORD}',roles:['readWrite','userAdmin','dbAdmin']});",
                   "insert": "db=db.getSiblingDB('${MONGODB_DATABASE}');db.testData.insert({x:0});",
                   "createUser2": "db.createUser({user:'test_user2',pwd:'test_password2',roles:['readWrite']});"}

        self.run('{} --eval "{}"'.format(self.MONGO_ADMIN_CMD, queries["dropUser"]))
        self.run('{} --eval "{}"'.format(self.MONGO_ADMIN_CMD, queries["createUser1"]))
        self.run('{} --eval "{}"'.format(self.MONGO_ADMIN_CMD, queries["insert"]))
        self.run('{} --eval "{}"'.format(self.MONGO_CMD, queries["createUser2"]))

if __name__ == '__main__':
    main()
