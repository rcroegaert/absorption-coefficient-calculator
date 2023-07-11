## About

The classes for each absorber model used in the calculator are defined here. There is a base class "AbsorberModel" which
defines the basic structure of each model. Each model inherits from this base class and defines its own extra parameters.

There are 4 models of absorbers currently implemented, all can be found in [@Jimenez]:

  * Porous Absorber: Johnson-Champoux-Allard Model.
  * Porous Absorber: Delany-Bazley Model.
  * Microperforated Panel: Maa´s Model.
  * Air
  * Plate: Infinite Elastic Wall Model.


!!! Warning "Info"
    **The Delany & Bazley code is implemented but is not being used by the calculator.**

-------------------

::: src.models
  