# yuxichau.com — local dev + deploy helpers
# Docs: _scripts/README.md (dashboard pipeline), README.md (site)

.PHONY: build serve check refresh-dashboard deploy

build: ## Build the site into _site/
	bundle exec jekyll build

serve: ## Serve locally at http://localhost:4000
	bundle exec jekyll serve

check: build ## Build + verify key outputs exist
	test -f _site/index.html
	test -f _site/404.html
	test -f _site/assets/images/favicon.svg

refresh-dashboard: ## Fetch AA data, regenerate dashboard, commit+deploy if changed
	bash _scripts/refresh_dashboard.sh

deploy: ## Push to main + trigger CF Pages build (needs CLOUDFLARE_API_TOKEN)
	bash _scripts/deploy.sh