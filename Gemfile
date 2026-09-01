source "https://rubygems.org"

# This mirrors the exact gem versions GitHub Pages uses in production,
# so what builds here matches what GitHub Pages actually deploys.
gem "github-pages", group: :jekyll_plugins

# Windows and JRuby do not include zoneinfo files by default.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows.
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]
