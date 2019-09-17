library(tidyverse)
library(jsonlite)

courses <- fromJSON("../courses.json")

courses %>% 
  filter(Location != "To be announced") %>% 
  group_by(date) %>% 
  count() %>% 
  ungroup() %>% 
  mutate(diff = n - lag(n, default = first(n))) %>% 
  ggplot(aes(date, diff)) +
  geom_col() +
  coord_flip()

courses %>% 
  filter(Location == "To be announced") %>% 
  group_by(date) %>% 
  count() %>% 
  ungroup() %>% 
  mutate(diff = n - lag(n, default = first(n))) %>% 
  ggplot(aes(date, n)) +
  geom_col() +
  coord_flip()

# Finds number of courses with NA or "To be announced" locations, then
# takes differences to find out which were set to that.
fromJSON("../tba_calls.json") %>% 
  mutate(date = as.Date(date)) %>% 
  group_by(date) %>%
  filter(is.na(Location) | Location == "To be announced") %>% 
  count() %>% 
  ungroup() %>% 
  mutate(diff = n - lag(n, default = first(n))) %>% 
  ggplot(aes(date, -diff)) +
  geom_col() +
  scale_x_date(date_breaks = "1 day", date_labels =  "%b %d") +
  labs(title = "Number of courses whose locations were set for the first time")

# Number of classes that changed locations from the previous day
fromJSON("../date_differences.json") %>% 
  mutate(date = as.Date(date)) %>% 
  ggplot(aes(date, differences)) +
  geom_col() +
  scale_x_date(date_breaks = "1 day", date_labels =  "%b %d") +
  labs(title = "Number of courses whose locations were changed")
