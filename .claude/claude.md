# Claude Configuration

## MCP Servers

### Agent Supervisor
Using agent-supervisor for approval workflows and CSS rule management only.

```json
{
  "mcpServers": {
    "agent-supervisor": {
      "approvals": {
        "enabled": true
      },
      "cssRules": {
        "enabled": true
      }
    }
  }
}
```

## Notes
- Only using agent-supervisor MCP for approvals and CSS rules
- All other MCP features disabled
