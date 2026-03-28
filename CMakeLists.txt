cmake_minimum_required(VERSION 3.8)
project(yeast_ros2_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

execute_process(
  COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/msg

  COMMAND python3 ${PROJECT_SOURCE_DIR}/template/render_jinja.py --template ${PROJECT_SOURCE_DIR}/template/msg.j2 --src-dir ${PROJECT_SOURCE_DIR}/yeast-schema/data_definitions/ --dst-dir ${PROJECT_SOURCE_DIR}/msg/
  # BYPRODUCTS ${CMAKE_CURRENT_SOURCE_DIR}/generated/include/${PROJECT_NAME}/parameters.hpp ${CMAKE_CURRENT_SOURCE_DIR}/generated/src/parameters.cpp
)

file(GLOB_RECURSE message_sources CONFIGURE_DEPENDS 
RELATIVE "${PROJECT_SOURCE_DIR}" "${PROJECT_SOURCE_DIR}/msg/*.msg"
)

find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME} 
  ${message_sources}
  DEPENDENCIES geometry_msgs
)
ament_export_dependencies(rosidl_default_runtime)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # comment the line when this package is in a git repo and when
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
