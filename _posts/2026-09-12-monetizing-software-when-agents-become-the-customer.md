---
layout: single
title: "Monetizing Software When Agents Become the Customer"
date: 2026-09-12 09:00:00 -0000
tags: [Economics, Technology, AI]
author: Yu Xi Chau
---

I wrote earlier that software companies should expose themselves to agents or risk being bypassed, and that API usage was the natural replacement for per-seat pricing. I still believe the direction is right. I was too quick about the timing and about where the durable value sits.

The first lesson comes from the difference between Figma and X. Figma's REST API and plugin APIs make a design file a structured, programmable object. A developer can inspect files, work with layers, modify designs, and build products around the design system. The API does more than add an integration. It makes Figma part of a wider software ecosystem. [Figma's REST API documentation](https://developers.figma.com/docs/rest-api) describes the files, nodes, comments, and webhooks that are available to developers.

X shows a more direct form of monetization. Its developer platform publishes consumption-based billing for API requests rather than relying only on a fixed subscription. The value of the platform is partly the data and activity that other software wants to read or create. [X's developer platform](https://developer.x.com/exhibit) presents that model as pay per use.

The important point is not that every application should copy X's exact pricing. It is that an API can be both a distribution channel and a meter. When an agent reads a record, creates an object, searches a corpus, or triggers a workflow, the provider can charge for the activity that creates value.

Atlassian is moving in this direction through Rovo. Rovo sits on top of Jira, Confluence, and connected sources, while Atlassian measures AI use and enriched Teamwork Graph access in Rovo credits. The credits matter because they make the valuable part of the platform visible: the agent is paying for access to context, permissions, and actions inside a structured system. Atlassian's [Rovo overview](https://www.atlassian.com/software/rovo) and [usage documentation](https://support.atlassian.com/rovo/docs/rovo-usage-limits) explain the model.

This changes my view of the per-seat model. Seats will not disappear quickly. Humans still need accountability, permissions, support, and a place to review work. But seats are a poor unit for machine activity. A person may ask an agent to perform hundreds of actions, and a company may use many agents without adding the same number of employees. Credits or metered API calls fit that usage more closely.

The cost of building the layer around software is also falling. Coding agents can now connect an API, write a client, test a workflow, and repair a broken integration with less human effort. A company no longer needs to buy a complete suite simply because reproducing its interface would be expensive. It can assemble a narrower tool around the workflow it actually needs.

That puts pressure on software whose only moat is a collection of screens. The stronger moat is the platform underneath: a useful data model, years of records, permissions, relationships between objects, and workflows that customers trust. An agent can recreate a dashboard. It is much harder to recreate the history and structure that make the dashboard useful.

Blender is a helpful analogy. A coding agent does not need to learn every button in Blender's interface. It can work through Blender's Python API, make a change to a scene, render it, inspect the result, and try again. The abstraction layer preserves the depth of the application while giving a new kind of user a different way in. [Blender's Python API](https://docs.blender.org/api/current/) is the kind of interface that makes this possible.

The same pattern can apply to a financial model, a design system, a data warehouse, or a project graph. The product becomes a structured world with an API layer that exposes safe, inspectable operations. The human interface remains important, but it is no longer the only front door.

For software companies, the practical monetization plan is straightforward:

1. Keep the data model and permissions strong.
2. Expose a reliable API for reading, writing, searching, and executing actions.
3. Give developers and agents clear documentation, limits, and audit trails.
4. Meter the usage that consumes meaningful platform resources.
5. Keep human seats for governance, collaboration, and review.

The winning product may therefore have two customers. Humans pay for trust, coordination, and control. Agents pay for context and actions. The platform earns from both without pretending that a machine is another employee.

My earlier argument was right that software must become reachable to agents. I would now add a qualification: reachability alone is not a moat. The durable business is the platform that owns a valuable system of record, expresses it through a dependable abstraction layer, and charges when that layer is used.