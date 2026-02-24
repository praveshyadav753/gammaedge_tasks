# `wrap_model_call` Middleware in LangChain

`wrap_model_call` wraps the **model node entirely**, acting like a decorator around the model.  

## What Can Be Modified?

The `ModelRequest` object contains:

- `state`  
- `messages`  
- `tools`  
- `model`  
- `response_format`  
- `runtime`  

You can **override properties** without mutating global state:

```python
request = request.override(
    model=new_model,
    tools=filtered_tools,
    response_format=new_schema
)
```

> This returns a new request object for **this call only**, leaving the global request intact.

## How It Works

```python
@wrap_model_call
def logging_middleware(request, handler):
    print("Before model call")
    
    response = handler(request)  # ← model gets called here
    
    print("After model call")
    return response
```

# Application Examples

### 1. Cost Optimization by Model Selection

```python
@wrap_model_call
def route_by_complexity(request, handler):
    tokens = sum(len(m.content) for m in request.messages)

    if tokens > 4000:
        request.model = advanced_model
    else:
        request.model = cheap_model

    return handler(request)
```

### 2. Retry Middleware Before Failure

```python
@wrap_model_call
def retry_middleware(request, handler):
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise
```

### 3. Cost Monitoring

```python
@wrap_model_call
def cost_tracker(request, handler):
    response = handler(request)

    usage = response.usage  # token usage info
    log_to_db(user_id=request.metadata["user_id"], usage=usage)

    return response
```

# 🔥 Core Difference

| Middleware Type | What It Intercepts |
|-----------------|-----------------|
| ✅ `wrap_model_call` | Intercepts **one single LLM call** |
| ✅ `before_agent`     | Intercepts the **entire agent run before it starts** |