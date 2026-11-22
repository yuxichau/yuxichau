---
layout: default
title: About
seo_title: About Yu Xi Chau | Systems Journal
description: Yu Xi Chau’s background in AI delivery, data science, physics and complexity science.
permalink: /about/
---
<div class="sj-about">
  <div class="sj-about-intro">
    <div class="sj-about-heading">
      <p class="sj-kicker">About</p>
      <h1>Yu Xi Chau</h1>
    </div>
    <figure class="sj-about-portrait"><img src="{{ '/assets/images/bio-photo-20260912.png' | relative_url }}" alt="Portrait of Yu Xi Chau" width="768" height="1024"><figcaption>Hong Kong</figcaption></figure>
    <div class="sj-about-summary">
      <p class="sj-about-lede">I build AI systems and help teams put them to work.</p>
      <p>I lead generative AI delivery at FWD Group. My route into AI started with physics and complexity science.</p>
    </div>
  </div>
  <section class="sj-about-journey" aria-labelledby="journey">
    <div class="sj-about-journey-heading">
      <h2 id="journey">Where I’ve Been</h2>
      <a href="#skills">Browse all skills ↓</a>
    </div>
    <ol class="sj-about-timeline" role="list">
      <li class="sj-about-current">
        <p class="sj-about-date"><time datetime="2025">2025</time> – Present</p>
        <div>
          <h3>FWD Group</h3>
          <p class="sj-about-role">Assistant Vice President, GenAI Digital Delivery</p>
          <p class="sj-about-detail">I’ve built on my MLOps experience as Product Owner for FWD’s AIOps platform. I also lead work on automating parts of software delivery with generative AI and contribute to AI governance. I work with business and engineering teams to decide where AI is worth adopting and what it takes to run it responsibly.</p>
          {% include about-stop-skills.html stop="fwd" %}
        </div>
      </li>
      <li>
        <p class="sj-about-date"><time datetime="2022">2022</time> – <time datetime="2025">2025</time></p>
        <div>
          <h3>AIA Hong Kong</h3>
          <p class="sj-about-role">Associate Director, Data Science Product &amp; AI</p>
          <p class="sj-about-detail">I owned MLOps and was a go-to person for AI governance. I led the team that built our machine learning platform and helped define how teams would deploy, run and govern models. I also led some of our first generative AI applications for insurance distribution.</p>
          {% include about-stop-skills.html stop="aia" %}
        </div>
      </li>
      <li>
        <p class="sj-about-date"><time datetime="2021">2021</time> – <time datetime="2022">2022</time></p>
        <div>
          <h3>Swire Properties</h3>
          <p class="sj-about-role">Data Services Lead</p>
          <p class="sj-about-detail">I moved into data services at Swire, broadening my work to include data modelling, data management and engineering alongside advanced analytics. I led the work to bring customer data together so teams could use it more reliably and protect it better.</p>
          {% include about-stop-skills.html stop="swire" %}
        </div>
      </li>
      <li>
        <p class="sj-about-date"><time datetime="2017">2017</time> – <time datetime="2021">2021</time></p>
        <div>
          <h3>A.S. Watson Group</h3>
          <p class="sj-about-role">Data Science Manager</p>
          <p class="sj-about-detail">I built and led a data science team that worked with retail teams on practical problems in personalisation, pricing and supply chain.</p>
          {% include about-stop-skills.html stop="watson" %}
        </div>
      </li>
      <li>
        <p class="sj-about-date"><time datetime="2016">2016</time> – <time datetime="2017">2017</time></p>
        <div>
          <h3>Hong Kong Jockey Club</h3>
          <p class="sj-about-role">Assistant Big Data Analytics Manager</p>
          <p class="sj-about-detail">I moved back to Hong Kong for personal reasons just as machine learning was finding more practical uses. Data science gave me a way to apply my technical background to business problems, and I found myself building an analytics team from the outset.</p>
          {% include about-stop-skills.html stop="hkjc" %}
        </div>
      </li>
      <li>
        <p class="sj-about-date"><time datetime="2010">2010</time>, <time datetime="2015">2015</time></p>
        <div>
          <h3>University of Warwick</h3>
          <p class="sj-about-role">MSc and PhD in Complexity Science</p>
          <p class="sj-about-detail">I started with a master’s at Warwick’s Complexity Science Doctoral Training Centre and stayed for a PhD. It took some exploring before I settled on interacting particle systems, working with Professor Stefan Grosskinsky and Professor Colm Connaughton.</p>
          <a class="sj-about-project" href="{{ '/projects/explosive-condensation/' | relative_url }}">Explore my interactive guide to explosive condensation <span aria-hidden="true">→</span></a>
          {% include about-stop-skills.html stop="warwick" %}
        </div>
      </li>
      <li>
        <p class="sj-about-date"><time datetime="2009">2009</time></p>
        <div>
          <h3>Imperial College London</h3>
          <p class="sj-about-role">MSci in Physics · Integrated undergraduate master’s</p>
          <p class="sj-about-detail">For my final-year project with Prof. K. Christensen, I looked at self-organised criticality in ant colonies. I also became interested in solid-state physics and statistical mechanics, which drew me towards complexity science at Warwick.</p>
          {% include about-stop-skills.html stop="imperial" %}
        </div>
      </li>
    </ol>
  </section>
  <section class="sj-about-skills" aria-labelledby="skills">
    <h2 id="skills" tabindex="-1">Skills I’ve Built</h2>
    <p class="sj-about-skills-deck">Everything tagged in the timeline, grouped by category.</p>
    <div class="sj-about-skills-grid">
      {%- assign all_skills = '' | split: ',' %}
      {%- for stop in site.data.about_skills.stops %}
        {%- assign all_skills = all_skills | concat: stop[1] %}
      {%- endfor %}
      {%- for category in site.data.about_skills.categories %}
        {%- assign category_skills = all_skills | where: 'category', category[0] | map: 'name' | uniq | sort_natural %}
      <section class="sj-about-skill-card sj-skill-{{ category[0] }}" aria-labelledby="skills-{{ category[0] }}">
        <h3 id="skills-{{ category[0] }}">{{ category[1] | escape }}</h3>
        <div class="sj-about-skill-chips">
          {%- for skill in category_skills %}
          <span class="sj-about-skill-chip">{{ skill | escape }}</span>
          {%- endfor %}
        </div>
      </section>
      {%- endfor %}
    </div>
  </section>
  <section class="sj-about-elsewhere" aria-labelledby="about-writing">
    <h2 id="about-writing">What I write about</h2>
    <p>I write about <a href="{{ '/topics/ai-systems/' | relative_url }}">building AI systems</a>, <a href="{{ '/topics/ai-governance/' | relative_url }}">governing them</a> and <a href="{{ '/topics/ai-application/' | relative_url }}">putting them to use</a>. My <a href="{{ '/projects/' | relative_url }}">side projects</a> explore history, maths and data.</p>
    <div class="sj-about-contact">
      <p>My CV is available upon request.</p>
      <a href="https://www.linkedin.com/in/yuxichau/">Get in touch on LinkedIn <span aria-hidden="true">↗</span></a>
    </div>
    <p class="sj-about-links"><a href="https://github.com/yuxichau">GitHub ↗</a><a href="{{ '/feed.xml' | relative_url }}">RSS ↗</a></p>
    <p class="sj-disclaimer">The views expressed here are my own and do not represent FWD Group or any other employer.</p>
  </section>
</div>
