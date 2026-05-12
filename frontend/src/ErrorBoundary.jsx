import React from 'react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 40, color: "white", background: "#990000", height: "100vh", overflow: "auto" }}>
          <h2>Something went wrong in the React App.</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {this.state.error && this.state.error.toString()}
            {"\n\n"}
            {this.state.error && this.state.error.stack}
          </pre>
        </div>
      );
    }
    return this.props.children;
  }
}
