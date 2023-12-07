### Developer notes

The A4_PROJECT_TOPICS tuples in the settings, have been moved to a dedicated enum class, TopicEnum. 
The new enum is a django model.TextChoices, which is a subclass of Enum. It allows for dynamic translations depending on the language settings of the django project. It is also more flexible to work with the enum values, label and code properties depending on where and how these are called in the code. 

The new TopicEnum is part of the `meinberlin.apps.contrib` app, and its path is set in the `meinberlin.config.settings.base`. 
 We can import the path from the settings as a string with `import_string` if necessary. 

see [topic_enums](https://github.com/liqd/adhocracy4/blob/main/docs/topic_enums.md) in adhocracy4.
