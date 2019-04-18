# -*- coding: utf-8 -*-
from draft_game import CardCollection
from table_draw import CollectionDraw

coll = CardCollection.generate()
print(coll.sorted())

input()

table = CollectionDraw(coll)
print(table.format())
