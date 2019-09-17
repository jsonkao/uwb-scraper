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

# Number of courses assigned a location by day
recourses <- fromJSON("../reassigned_calls.json") %>% 
  mutate(date = as.Date(date))
recourses %>% 
  group_by(date) %>%
  filter(is.na(Location) | Location == "To be announced") %>% 
  count() %>% 
  ungroup() %>% 
  mutate(diff = n - lag(n, default = first(n))) %>% 
  ggplot(aes(date, diff)) +
  geom_col() +
  scale_x_date(date_breaks = "1 day", date_labels =  "%b %d") +
  coord_flip()
