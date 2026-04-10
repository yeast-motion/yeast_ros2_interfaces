# yeast_ros2_interfaces - Growth Opportunities

## Improvement Opportunities

### 1. Sync `OdometrySample` schema with C++ type
Add `pose_valid`, `velocity_valid`, and `acceleration_valid` boolean fields to `OdometrySample.schema.json` to match the C++ `OdometrySample` class. Without these, the ROS2 message helper in `yeast_ros2_utilities_node` silently drops validity data during conversion.

### 2. Add `accel` to `SwerveModuleCommand` schema
Add the `accel` field to `SwerveModuleCommand.schema.json` to match the C++ type's `accel` member.

### 3. Add `Trajectory` message definition
There is no schema or message for `Trajectory`, which is a key data structure in the system. Currently trajectories must be passed as raw JSON strings.

### 4. Add `string` to the type map in `render_jinja.py`
Add `'string': 'string'` to the `type_map` dict at line 24 for completeness and safety.

### 5. Add message documentation/comments
The generated `.msg` files have no field descriptions. The Jinja template could pull `"description"` from the schema properties and emit ROS2 comment lines.

## Architectural Enhancements

### 6. Validate schemas against JSON Schema spec
None of the schemas have `"required"` fields, meaning all properties are optional per the JSON Schema specification. Adding `"required"` arrays would enable validation.

### 7. Add service/action definitions
The interfaces package only has messages (topics). For operations like "reset odometry" or "begin trajectory", ROS2 services or actions would provide request/response semantics.

### 8. Use a single source of truth for type definitions
The schemas, C++ types, ROS2 messages, and msg helper conversions are all manually kept in sync. A single definition (e.g., the schema) should auto-generate all others to prevent drift.

## Testing Gaps

### 9. No tests for the code generator
`render_jinja.py` has no tests. Edge cases to verify:
- Schema with nested `$ref` chains
- Schema with array types of `$ref` items
- Schema with properties that have both `type` and `$ref`
- Empty schema files (the skip logic at line 31)
- Schemas with unmapped types
