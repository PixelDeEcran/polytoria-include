# Polytoria-Include

This is a very basic CLI to merge multiple lua files in one.

# Installation

You will need Python3, Pipx and Poetry.
To install polytoria-include, clone this repo and then execute the following commands:

```
poetry install
pipx install .
```

# Usage

```
polytoria-include <source> <out>
```

To include a file, use
```
---#include <path>
```
where `<path>` is the path of the lua file relative to the root dir.
The root dir is the folder containing the source file.

For instance, let's say I have the following file tree:

```
myproject
 |- server
 |   |- PlayerData.lua
 |
 |- client
 |   |- CarController.lua
 |   |- CarRenderer.lua
 |   
 |- shared
 |   |- Globals.lua
 |   |- Settings.lua
 |
 |- Client.client.lua
 |- Server.server.lua
```

In CarController.lua, I can write:
```
---#include shared/Settings.lua
---#include client/CarRenderer.lua
```


Inclusion only happens once, so any inclusion of the same file in another file will be ignored.
Cyclic dependency will throw error.


You can also add code specific to client or server. It allows to merge client and server logic in one file.

```lua
print("Both Server and Client will see this message.")

---#if client then
print("Only Client will see this message.")
---#end

---#if server then
print("Only Server will see this message.")
---#end
```

If the source file ends with `.client.lua`, the server logic will be ignored, otherwise, by default the client logic will be ignored. By convention, the server source file ends with `.server.lua` .