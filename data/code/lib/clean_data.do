program main
  import delim using "output/data_merged.csv", clear
  plot_data
  clean_data
  export delim "output/data_cleaned.csv", replace
end

program plot_data
  histogram chips_sold
  graph export "output/chips_sold.pdf", replace
end

program clean_data
  replace chips = . if chips_sold == -999999
end

main()
