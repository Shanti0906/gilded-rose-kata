# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from item import Item
from gilded_rose import GildedRose

NORMAL_ITEM = "+5 Dexterity Vest"
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
CONJURED = "Conjured Mana Cake"


def run(name, sell_in, quality, days=1):
    item = Item(name, sell_in, quality)
    shop = GildedRose([item])
    for _ in range(days):
        shop.update_quality()
    return item


# normal items

def test_normal_item_degrades_by_one():
    item = run(NORMAL_ITEM, sell_in=10, quality=20)
    assert item.sell_in == 9
    assert item.quality == 19


def test_normal_item_degrades_faster_once_expired():
    item = run(NORMAL_ITEM, sell_in=0, quality=10)
    assert item.sell_in == -1
    assert item.quality == 8


def test_normal_item_on_sell_date_still_only_drops_by_one():
    item = run(NORMAL_ITEM, sell_in=1, quality=10)
    assert item.sell_in == 0
    assert item.quality == 9


def test_normal_item_quality_floor():
    assert run(NORMAL_ITEM, sell_in=5, quality=0).quality == 0
    assert run(NORMAL_ITEM, sell_in=0, quality=0).quality == 0
    assert run(NORMAL_ITEM, sell_in=1, quality=1, days=3).quality == 0


# aged brie

def test_brie_increases_with_age():
    item = run(AGED_BRIE, sell_in=10, quality=20)
    assert item.sell_in == 9
    assert item.quality == 21


def test_brie_quality_cap():
    assert run(AGED_BRIE, sell_in=10, quality=50).quality == 50


def test_brie_increases_faster_after_sell_date():
    item = run(AGED_BRIE, sell_in=0, quality=40)
    assert item.sell_in == -1
    assert item.quality == 42


def test_brie_still_capped_at_50_past_sell_date():
    item = run(AGED_BRIE, sell_in=-1, quality=48)
    assert item.sell_in == -2
    assert item.quality == 50


# sulfuras

def test_sulfuras_never_changes():
    item = run(SULFURAS, sell_in=0, quality=80)
    assert item.sell_in == 0
    assert item.quality == 80


def test_sulfuras_never_changes_over_time():
    item = run(SULFURAS, sell_in=-5, quality=80, days=5)
    assert item.sell_in == -5
    assert item.quality == 80


# backstage passes

def test_backstage_more_than_10_days_out():
    item = run(BACKSTAGE, sell_in=15, quality=20)
    assert item.sell_in == 14
    assert item.quality == 21


def test_backstage_10_days_or_fewer():
    item = run(BACKSTAGE, sell_in=10, quality=20)
    assert item.sell_in == 9
    assert item.quality == 22


def test_backstage_5_days_or_fewer():
    item = run(BACKSTAGE, sell_in=5, quality=20)
    assert item.sell_in == 4
    assert item.quality == 23


def test_backstage_last_day():
    item = run(BACKSTAGE, sell_in=1, quality=20)
    assert item.sell_in == 0
    assert item.quality == 23


def test_backstage_worthless_after_concert():
    item = run(BACKSTAGE, sell_in=0, quality=20)
    assert item.sell_in == -1
    assert item.quality == 0

    # stays at 0, doesn't go negative
    item = run(BACKSTAGE, sell_in=0, quality=20, days=3)
    assert item.quality == 0


def test_backstage_quality_cap():
    item = run(BACKSTAGE, sell_in=5, quality=49)
    assert item.quality == 50


# conjured - the new feature

def test_conjured_degrades_twice_as_fast():
    item = run(CONJURED, sell_in=10, quality=20)
    assert item.sell_in == 9
    assert item.quality == 18  # normal item would only drop to 19


def test_conjured_degrades_by_4_once_expired():
    item = run(CONJURED, sell_in=0, quality=20)
    assert item.sell_in == -1
    assert item.quality == 16


def test_conjured_quality_floor():
    assert run(CONJURED, sell_in=0, quality=1).quality == 0
