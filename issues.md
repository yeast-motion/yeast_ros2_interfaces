# yeast_ros2_interfaces - Issues

## Bugs / Correctness Problems

### 1. `OdometrySample.msg` is missing validity fields present in C++ type
The generated `msg/OdometrySample.msg` only has `Pose2D pose`, `Twist2D velocity`, `Twist2D acceleration` -- no `pose_valid`, `velocity_valid`, or `acceleration_valid` fields. But the C++ `OdometrySample` class in yeastcpp has all three validity booleans. This means validity information is lost when converting `OdometrySample` through ROS2 messages.

The root cause is that `OdometrySample.schema.json` only has `$ref` properties (pose, velocity, acceleration) and no primitive `"type"` properties, so the Jinja template skips the validity fields. The schema is out of sync with the C++ type.

### 2. `SwerveModuleCommand.msg` is missing the `accel` field
The generated `msg/SwerveModuleCommand.msg` only has `speed` and `theta`. The C++ `SwerveModuleCommand` has an `accel` field. The schema `SwerveModuleCommand.schema.json` also only has `speed` and `theta`, so the schema is the source of truth mismatch.

### 3. `AbsolutePoseEstimate.json` naming inconsistency
The file `yeast-schema/data_definitions/AbsolutePoseEstimate.json` does not follow the `.schema.json` naming convention used by all other schema files. This works because `render_jinja.py:20` globs `*.json`, but it is a latent fragility.

### 4. `render_jinja.py` type mapping is incomplete
`template/render_jinja.py:24-28`: The `type_map` only handles `number`, `boolean`, and `integer`. If a schema uses `string` type (which `FollowerStatus` does for the array items), the type falls through. In the `FollowerStatus` case this works because ROS2 understands `string`, but other unmapped types could silently produce invalid `.msg` files.

### 5. `render_jinja.py` uses `type` as a variable name
`template/render_jinja.py:45,48,50,53`: The variable `type` shadows the Python built-in `type()` function. Not a bug but a code smell that could cause subtle issues if the code is extended.

## Code Smells

### 6. All schemas use the same `$id` placeholder
Every schema file uses `"$id": "https://example.com/product.schema.json"` (e.g., `Pose2D.schema.json:3`). These should be unique per schema if `$id` is ever used for resolution.

### 7. No `sensor_msgs` dependency actually used
`CMakeLists.txt:11`: `find_package(sensor_msgs REQUIRED)` is included but no message depends on `sensor_msgs`.

### 8. Generated `.msg` files are checked into the repo
The `msg/` directory contains generated files that are produced by `render_jinja.py` at build time (`CMakeLists.txt:13-17`). These should either be gitignored or the generation step should be the sole source of truth.
