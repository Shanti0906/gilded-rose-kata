# -*- coding: utf-8 -*-

MIN_QUALITY = 0
MAX_QUALITY = 50

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
CONJURED_PREFIX = "Conjured"  # e.g. "Conjured Mana Cake" - matches any conjured item, not just this one


def _clamp(quality):
    return max(MIN_QUALITY, min(MAX_QUALITY, quality))


class NormalItemUpdater:
    DEGRADE_RATE = 1

    def update(self, item):
        item.quality = _clamp(item.quality - self.DEGRADE_RATE)
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = _clamp(item.quality - self.DEGRADE_RATE)


class ConjuredItemUpdater(NormalItemUpdater):
    # same as normal, just twice the degrade rate
    DEGRADE_RATE = 2


class AgedBrieUpdater:
    def update(self, item):
        item.quality = _clamp(item.quality + 1)
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = _clamp(item.quality + 1)


class SulfurasUpdater:
    def update(self, item):
        pass  # legendary, never changes


class BackstagePassUpdater:
    def update(self, item):
        if item.sell_in < 6:
            bonus = 3
        elif item.sell_in < 11:
            bonus = 2
        else:
            bonus = 1

        item.quality = _clamp(item.quality + bonus)
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = 0  # worthless after the concert


def _updater_for(item):
    if item.name == AGED_BRIE:
        return AgedBrieUpdater()
    if item.name == SULFURAS:
        return SulfurasUpdater()
    if item.name == BACKSTAGE_PASSES:
        return BackstagePassUpdater()
    if item.name.startswith(CONJURED_PREFIX):
        return ConjuredItemUpdater()
    return NormalItemUpdater()


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            _updater_for(item).update(item)
