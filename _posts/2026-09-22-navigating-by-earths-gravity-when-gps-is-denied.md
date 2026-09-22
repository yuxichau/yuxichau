---
layout: single
title: "Navigating by Earth's gravity when GPS is denied"
date: 2026-09-22 05:00:00 -0000
tags: [Technology]
author: Yu Xi Chau
---

I like the idea of navigating by Earth's gravity when GPS is unavailable. It has the obvious benefit of being passive and difficult to jam, and it is also a wonderfully nerdy way to find your position. A gravimeter measures tiny variations in gravitational acceleration and a navigation system matches them against a map, much as a hiker matches a landscape against a chart. [Q-CTRL describes a recent GPS-free gravimetric navigation trial](https://q-ctrl.com/blog/q-ctrl-achieves-worlds-first-gps-free-quantum-gravimetric-navigation-demonstration-in-maritime-field-trial), while earlier gravity-mapping work showed how much the usefulness depends on the resolution of the map and the sensor.

My instinct is that the engineering becomes difficult very quickly. A skyscraper or a large piece of infrastructure can create a local gravity signal measured in hundreds of microgals, which is large enough to complicate any attempt at metre-level positioning in a built-up area. The global reference map is another problem. [ESA's GOCE mission achieved roughly 1 mGal accuracy at a 100 km spatial resolution](https://www.esa.int/Applications/Observing_the_Earth/FutureEO/GOCE/ESA_launches_Earth_Explorer_mission_GOCE), not a street-level map, and the field changes as mass moves. [USGS records about 20,000 earthquakes around the world each year](https://www.usgs.gov/faqs/why-are-we-having-so-many-or-so-few-earthquakes-has-naturally-occurring-earthquake-activity), though only a fraction would matter to a particular navigation map. I may be missing clever filtering and sensor fusion that makes this practical. Positioning at roughly kilometre scale feels plausible; metre-level positioning everywhere feels like a much harder promise.
