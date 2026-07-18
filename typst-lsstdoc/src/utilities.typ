#let rubin-teal = rgb("#058b8c")
#let muted-teal = rgb("#087273")
#let light-teal = rgb("#e8f5f5")
#let url-blue = rgb("#005ea8")

#let rubin-logo-path = "../assets/rubin-logo.svg"

// Shared appearance of external links.
#let url-styled(body) = underline(
  stroke: 0.45pt + url-blue,
  text(fill: url-blue, body),
)

#let series-data = yaml("../data/series.yaml")
#let series-map = series-data.at("series")
#let controlled-series = series-data.at("controlled")

#let validate-series(series) = assert(
  series in series-map,
  message: "Unsupported Rubin document series: " + series,
)

#let series-label(series) = {
  validate-series(series)
  series-map.at(series)
}

#let value-or(data, key, default: none) = data.at(key, default: default)

#let nonempty(value) = value != none and value != ""
