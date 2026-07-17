#let rubin-teal = rgb("#058b8c")
#let muted-teal = rgb("#087273")
#let light-teal = rgb("#e8f5f5")
#let url-blue = rgb("#005ea8")

#let series-data = yaml("../data/series.yaml")
#let series-map = series-data.at("series")

#let series-label(series) = {
  assert(
    series-map.keys().contains(series),
    message: "Unsupported Rubin document series: " + series,
  )
  series-map.at(series)
}

#let value-or(data, key, default: none) = data.at(key, default: default)

#let nonempty(value) = value != none and value != ""
