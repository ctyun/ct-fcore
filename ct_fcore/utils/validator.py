# -*- coding:utf-8 -*-
import re

def required(value):
    return len(value)!=0


def minLength(value, minL):
    return len(value)>= int(minL)


def maxLength(value, maxL):
    return len(value)<= int(maxL)


def phone(vlaue):
    reg = re.compile(r"1\d{10}")
    return reg.findall(vlaue)


def email(value):
    reg = re.compile(r'^.+@([^.@][^@]+)$')
    return reg.findall(value)


def same(value, value2):
    return value == value2


def validate(pairs):
    for value, rules in pairs.items():
        for rule in rules:
            if len(rule.split(":"))==1:
                if not eval(rule.split(":")[0])(value):
                    raise Exception("you shall not pass!")
            elif len(rule.split(":")) == 2:
                if not eval(rule.split(":")[0])(value, rule.split(":")[1]):
                    raise Exception("you shall not pass!")
