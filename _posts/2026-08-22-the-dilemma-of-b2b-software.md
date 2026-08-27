---
layout: single
title: "The Dilemma of B2B Software in the Agent-First Age"
date: "2026-08-22 03:04:20 -0000"
tags: [Economics, Technology, AI]
author: Yu Xi Chau
---

I read a post by Paul Graham on X a while back. It was mostly about something else, but somewhere in the middle he made a one-sentence statement about the future of software: it would be agent-first. He did not elaborate. I cannot find the post now, and I would not swear to his exact wording, but the sentence has stayed with me. The more I think about it, the more it looks like the future of the whole software industry.

The core tension is simple. People don't really want software anymore. They want something that can be connected to an agent. It is like the age of electrification. Once the grid arrived, it became inconceivable for a factory not to connect to it. You could keep your steam engines running forever and it would not matter, because every new factory was built to plug into the grid, and the whole economy quietly moved to the standard the grid set. Software that cannot plug into the agent grid gets abandoned, no matter how good it is.

Assuming that assumption is true, that agent-first is here to last, then look at what software companies are betting on. A lot of it still assumes the old world, and I have seen how that ends. Back when I was working in retail, I was horrified to learn that our Chinese arm was sharing all our data with the Chinese platforms. All of it. Customer data, sales data, going outside the company. It felt like a betrayal of everything you are taught about guarding customer information. Little did I know then that they had no choice. It was already becoming the norm. If you want to sell in that ecosystem, the platform gets the data, and the traffic flows to whoever is plugged in. Standing outside the door is a decision you don't get to make twice. The agent ecosystem is becoming that front door for software, exactly the same way. If your service cannot be reached by an agent, it doesn't matter how good your app is. Nobody walks to doors anymore. They send agents.

Software companies now face a strange pair of facts. If they don't expose their services to agents, the traffic dries up, exactly like the WeChat and Alibaba holdouts. But if they do expose their services, then all the native AI they build into their own products is in vain. Not because the features are bad, but because they can't be a moat. People are bringing their own agents to your system. Your carefully built chat assistant is competing with the agent your customer already owns, and losing, because that agent already knows how to talk to everything else in the customer's life.

The way to monetize this is API usage. X switched to this quickly: a metered, paid API, and it turned out to be one of the more honest business models in tech. It works naturally for marketplaces and platforms, where the value comes from adoption. You charge per call, per read, per transaction. The agent is just another customer, and it is a customer that never sleeps, never churns, and never needs a sales call.

Now look at the closed B2B systems, and you see the dilemma nobody has a good answer for. Take Atlassian. Jira and Confluence are closed systems of record. But a company does not need to be on Atlassian to do its job. Software is incredibly cheap now. The actual value was never the tool, it was the product vision encoded in it: the workflow, the fields, the reports. And here is the uncomfortable part. A company with a good product manager and AI agents can now tailor-make its own Jira, its own Confluence, and keep exactly the workflow it wants. I struggle to see the value of the closed suite two or three years down the line. Which is also why Atlassian's AI strategy of folding more native AI into its products is a miss. It improves the app for humans, but the coming customers are agents, and agents don't need your app. They need your API.

The per-seat model is the tell. Every Atlassian license is priced per human. But the number of agents in a company is about to be several times the number of humans, and agents don't consume software in a way that respects seat counts. Either your software is a service agents call, priced per call, or it's a closed room that agents simply walk around.

If I were a CIO at a mid-size company, here is a simple plan for replacing Jira and Confluence, and it is not even ambitious:

1. **Own the data model.** Issues, sprints, documents. One Postgres schema, small, and yours.
2. **Expose a thin API over it.** FastAPI or Express with an OpenAPI spec. The spec is the real product, because that is where the agents live.
3. **Build a minimal UI for the humans.** A dashboard, a way to create and comment. It doesn't need to be beautiful. Jira's UI was never the reason anyone stayed.
4. **Wire in your agents.** Bring your own: the same agent your engineers already use, pointed at the API. Workflows become prompts and permissions, not admin panel configuration.

High level numbers for a 500-person company, using Hong Kong rates for the people cost:

| Item | Cost |
|---|---|
| Atlassian Premium (Jira + Confluence) | ~$26/user/month, roughly **$160K/year** |
| Atlassian Enterprise | custom quote, expect **$250K-$400K/year** |
| Build once (PM + 2 mid engineers, 6-8 weeks) | **$40K-$50K** |
| Run on AWS (EC2, RDS, S3, ALB) | **$15K-$25K/year** |
| Maintenance (half a mid-level engineer; HK$50K/month ≈ US$77K/year FTE) | **$35K-$40K/year** |

Year one comes to $90K-$115K, against $160K+ for the license alone. Years after that it's roughly $50K-$65K a year, and the license is a floor that keeps rising. There is no per-seat bill that grows as you hire, and no per-agent bill that grows when your agents outnumber your people.

The catch is real. You are now maintaining it, and software maintenance is eternal. But the maintenance is cheap, it is yours, and you can change the workflow as fast as your product manager can think of it, which is the entire reason companies bought Jira in the first place.

And this is just the beginning. These are rough numbers at today's prices, and the scaffolding around agents improves by the week. The version of this plan we will have by November will be cheaper, better, and mostly built by the agents themselves. The question for every software company is the same: are you building services for the new customers, or a room that nobody will walk into?