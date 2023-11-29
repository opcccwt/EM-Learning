package edu.ucla.belief.ace;

/**
 * An exception that evaluation and differentiation may throw when underflow
 * occurs.
 * 
 * @author Mark Chavira
 */

public class UnderflowException extends Exception {
  /**
   * Default constructor.
   **/
  public UnderflowException() {}

  // Just to get rid of warning.
  private static final long serialVersionUID = 1L;
}
