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

!!! Failure "Error"
    **The values calculated for the Plate Model are not consistent with the goal of this tool.
    When using the plate model, the transmission loss is of importance, not the absorption.**
-------------------

::: src.models
  