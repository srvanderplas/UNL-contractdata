library(tidyverse)

df <- read_csv("Scraped_Contracts.csv") %>%
  select(-"0") %>%
  rename("Row" = ...1) %>%
  set_names(make.names(names(.))) %>%
  mutate_at(.vars = vars(matches("Date")), .funs = mdy) %>%
  mutate(Amount = parse_number(Amount)) %>%
  arrange(Amount, Begin.Date, desc = T)
write_csv(df, "Cleaned_Contracts.csv")

Vendor_summary <- df %>%
  group_by(Vendor) %>%
  summarize(Amount = sum(Amount), Begin.Date = min(Begin.Date)) %>%
  arrange(desc(Amount))
write_csv(Vendor_summary, "Vendor_Summary.csv")
