# CNC Calculator Development Guidelines

## Project Overview
This is a full-stack CNC tool management application with Next.js frontend and FastAPI backend, designed for CNC machinists to create, manage, and export tool profiles compatible with Fusion 360.

## Architecture Principles

### Frontend (Next.js)
- Use App Router for all new pages and components
- Prefer TypeScript strict mode with proper type definitions
- Use Tailwind CSS for styling with custom component classes
- Implement real-time validation with Zod schemas
- Follow React best practices: hooks, proper state management, memoization when needed

### Backend (FastAPI)
- Use async/await patterns throughout
- Implement proper error handling with structured logging
- Use Pydantic for data validation and serialization
- Follow RESTful API design principles
- Implement comprehensive input validation

### Database
- Use PostgreSQL with SQLAlchemy ORM
- Store tool geometry as JSON for flexibility
- Implement soft deletes for data integrity
- Use proper indexing for performance

## Code Standards

### TypeScript/JavaScript
- Use strict TypeScript configuration
- Prefer interfaces over types for object shapes
- Use proper error boundaries and error handling
- Implement proper loading states and error states
- Use React.memo and useMemo for performance optimization

### Python
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and returns
- Implement proper async/await patterns
- Use structured logging with context
- Write comprehensive docstrings

### CSS/Styling
- Use Tailwind CSS utility classes
- Create reusable component classes in globals.css
- Follow mobile-first responsive design
- Use CSS custom properties for theming
- Implement proper focus states for accessibility

## Tool Management Features

### Tool Types
1. **End Mill**: Square end cutting tool with helix angle and corner radius
2. **Ball End Mill**: Spherical end for 3D contouring
3. **Chamfer Mill**: Angled cutting tool for edge chamfering
4. **Drill**: Pointed tool for hole drilling
5. **Reamer**: Precision finishing tool
6. **Thread Mill**: Tool for creating threads

### Validation Rules
- All tools require diameter, flute length, and overall length
- Geometry relationships must be validated (e.g., flute length < overall length)
- Tool-specific validations (e.g., ball end mill tip radius = diameter/2)
- Fusion 360 compatibility checks

### Export Formats
- **Fusion 360 JSON**: Direct import into Fusion 360 tool library
- **CSV**: Compatible with Excel and other CAM software
- Support for metric (mm) and imperial (inches) units

## Development Workflow

### Setup
1. Run `make setup` to install dependencies and configure environment
2. Run `make db-up` to start local database
3. Run `make dev` to start development servers

### Testing
- Write unit tests for all business logic
- Implement integration tests for API endpoints
- Use Playwright for end-to-end testing
- Maintain >80% code coverage

### Code Quality
- Run `make lint` before committing
- Use `make format` to format code
- Run `make type-check` for TypeScript validation
- Use `make security-scan` for vulnerability checks

## API Design

### Endpoints
- `GET /api/tools` - List tools with pagination and filtering
- `POST /api/tools` - Create new tool
- `GET /api/tools/{id}` - Get specific tool
- `PUT /api/tools/{id}` - Update tool
- `DELETE /api/tools/{id}` - Soft delete tool
- `POST /api/tools/{id}/validate` - Validate tool for Fusion 360
- `POST /api/tools/{id}/export` - Export tool
- `GET /api/tools/{id}/export/{export_id}/download` - Download export

### Error Handling
- Use proper HTTP status codes
- Return structured error responses
- Implement proper logging for debugging
- Use validation errors for user feedback

## Security Considerations

### Authentication
- Implement JWT-based authentication
- Use secure session management
- Implement proper CORS configuration
- Use environment variables for secrets

### Data Validation
- Validate all input data
- Sanitize user inputs
- Implement rate limiting
- Use proper SQL injection prevention

## Performance Optimization

### Frontend
- Use React.memo for expensive components
- Implement proper code splitting
- Use SWR for efficient data fetching
- Optimize bundle size with tree shaking

### Backend
- Use database connection pooling
- Implement proper caching with Redis
- Use async/await for I/O operations
- Implement proper pagination

## Monitoring and Logging

### Structured Logging
- Use structured logging with context
- Log all API requests and responses
- Implement proper error tracking
- Use correlation IDs for request tracing

### Health Checks
- Implement comprehensive health checks
- Monitor database connectivity
- Monitor Redis connectivity
- Provide metrics endpoints

## Deployment

### Development
- Use Docker Compose for local development
- Implement hot reloading for both frontend and backend
- Use local PostgreSQL and Redis instances

### Production
- Use AWS ECS for container orchestration
- Use RDS PostgreSQL for database
- Use ElastiCache Redis for caching
- Implement proper CI/CD with GitHub Actions

## Accessibility

### Frontend
- Implement proper ARIA labels
- Use semantic HTML elements
- Ensure keyboard navigation
- Implement proper focus management
- Use sufficient color contrast

### API
- Provide clear error messages
- Use proper HTTP status codes
- Implement proper CORS headers
- Provide API documentation

## Testing Strategy

### Unit Tests
- Test all business logic functions
- Test validation functions
- Test utility functions
- Mock external dependencies

### Integration Tests
- Test API endpoints
- Test database operations
- Test export functionality
- Test validation workflows

### End-to-End Tests
- Test complete user workflows
- Test tool creation process
- Test export functionality
- Test responsive design

## Documentation

### Code Documentation
- Write comprehensive docstrings
- Use proper TypeScript type definitions
- Document API endpoints with examples
- Maintain up-to-date README

### User Documentation
- Provide clear setup instructions
- Document all features and workflows
- Include troubleshooting guides
- Provide API documentation

## Common Patterns

### Frontend Components
```typescript
interface ComponentProps {
  // Define props with proper types
}

export default function Component({ prop1, prop2 }: ComponentProps) {
  // Use proper state management
  const [state, setState] = useState<StateType>(initialValue);
  
  // Implement proper error handling
  const { data, error, isLoading } = useSWR('/api/endpoint');
  
  // Use proper loading states
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <div className="component-container">
      {/* Use semantic HTML and proper accessibility */}
    </div>
  );
}
```

### Backend Services
```python
class ServiceClass:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def method_name(self, param: ParamType) -> ReturnType:
        """Comprehensive docstring explaining the method."""
        try:
            # Implement business logic
            result = await self._private_method(param)
            return result
        except Exception as e:
            logger.error("Error in method_name", error=str(e), param=param)
            raise HTTPException(status_code=500, detail="Internal server error")
```

### Database Models
```python
class Model(Base):
    __tablename__ = "table_name"
    
    id = Column(String, primary_key=True, index=True)
    # Define columns with proper types and constraints
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            # Include all relevant fields
        }
```

## Troubleshooting

### Common Issues
1. **Database Connection**: Check DATABASE_URL and ensure PostgreSQL is running
2. **Redis Connection**: Check REDIS_URL and ensure Redis is running
3. **CORS Issues**: Verify ALLOWED_ORIGINS configuration
4. **Build Errors**: Check Node.js and Python versions
5. **Type Errors**: Run type checking and fix TypeScript issues

### Debugging
- Use structured logging for debugging
- Check browser developer tools for frontend issues
- Use FastAPI's automatic documentation for API testing
- Monitor database queries and performance

## Future Enhancements

### Planned Features
- 3D tool visualization with Three.js
- Advanced tool performance calculations
- Tool library sharing and collaboration
- Integration with more CAM software
- Mobile app development

### Technical Improvements
- Implement GraphQL API
- Add real-time collaboration features
- Implement advanced caching strategies
- Add comprehensive monitoring and alerting
- Implement automated testing in CI/CD
