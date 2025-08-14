# WEE Interface
**UTCS-MI Code: [184] WEE Interface**

## Wisdom Evolution Engine Interface

### Learning APIs
- `POST /wee/learn` - Submit learning experience
- `GET /wee/knowledge` - Query knowledge base
- `POST /wee/pattern` - Register learning pattern
- `GET /wee/wisdom` - Get wisdom summary

### Knowledge Management
- `GET /wee/graph` - Knowledge graph structure
- `POST /wee/connect` - Create knowledge connections
- `PUT /wee/update` - Update knowledge node
- `DELETE /wee/prune` - Prune low-confidence knowledge

### Evolution Control
- `POST /wee/evolve` - Trigger evolution process
- `GET /wee/evolution/status` - Evolution status
- `PUT /wee/evolution/config` - Configure evolution parameters

### Integration Interfaces
- **DeMOS Integration**: Metrics-driven learning
- **AMOReS Integration**: Compliance-aware evolution
- **GAIA Integration**: Mission data learning