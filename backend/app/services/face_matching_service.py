"""
Face Matching Service - Core face recognition engine
Implements Euclidean distance-based face matching using embeddings
"""

import logging
from typing import List, Tuple, Optional
import numpy as np

from app.utils.constants import FACE_MATCH_THRESHOLD
from app.utils.exceptions import FaceMatchingError

logger = logging.getLogger(__name__)


class FaceMatchingService:
    """
    Service for face embedding matching using Euclidean distance.
    
    Uses pre-computed face embeddings (128-dimensional vectors) and
    finds the closest match using nearest neighbor search with a threshold.
    """

    @staticmethod
    def calculate_euclidean_distance(embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate Euclidean distance between two face embeddings.
        
        Args:
            embedding1: First face embedding (list of floats)
            embedding2: Second face embedding (list of floats)
            
        Returns:
            float: Euclidean distance between embeddings
            
        Raises:
            FaceMatchingError: If embeddings are invalid
        """
        try:
            # Convert to numpy arrays
            emb1 = np.array(embedding1, dtype=np.float32)
            emb2 = np.array(embedding2, dtype=np.float32)
            
            # Validate dimensions
            if emb1.shape != emb2.shape:
                raise FaceMatchingError(
                    message="Embedding dimensions do not match",
                    details=f"Expected same dimensions, got {emb1.shape} and {emb2.shape}"
                )
            
            # Calculate Euclidean distance using numpy
            # Distance = sqrt(sum((x_i - y_i)^2))
            distance = float(np.linalg.norm(emb1 - emb2))
            
            logger.debug(f"Calculated distance: {distance:.4f}")
            return distance
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error calculating distance: {str(e)}")
            raise FaceMatchingError(
                message="Failed to calculate distance",
                details=str(e)
            )

    @staticmethod
    def find_nearest_match(
        query_embedding: List[float],
        database_embeddings: List[Tuple[int, List[float]]],
        threshold: Optional[float] = None
    ) -> Optional[Tuple[int, float]]:
        """
        Find the nearest match in database using nearest neighbor search.
        
        Performs exhaustive search through all embeddings and returns
        the closest match if it's within the threshold.
        
        Args:
            query_embedding: Query face embedding (128D vector)
            database_embeddings: List of tuples (user_id, embedding)
            threshold: Distance threshold for match (uses default if None)
            
        Returns:
            Tuple of (user_id, distance) if match found, None otherwise
            
        Raises:
            FaceMatchingError: If search fails
        """
        if threshold is None:
            threshold = FACE_MATCH_THRESHOLD
        
        try:
            if not database_embeddings:
                logger.warning("No embeddings in database for comparison")
                return None
            
            min_distance = float('inf')
            best_match_id = None
            
            # Exhaustive search: compare with all database embeddings
            for user_id, db_embedding in database_embeddings:
                try:
                    distance = FaceMatchingService.calculate_euclidean_distance(
                        query_embedding,
                        db_embedding
                    )
                    
                    # Keep track of minimum distance
                    if distance < min_distance:
                        min_distance = distance
                        best_match_id = user_id
                        
                except FaceMatchingError:
                    # Skip invalid embeddings
                    logger.warning(f"Skipping invalid embedding for user {user_id}")
                    continue
            
            # Check if best match is within threshold
            if best_match_id is not None and min_distance <= threshold:
                logger.info(
                    f"Found match: user_id={best_match_id}, distance={min_distance:.4f}"
                )
                return (best_match_id, min_distance)
            
            logger.info(
                f"No match found. Best distance: {min_distance:.4f}, Threshold: {threshold}"
            )
            return None
            
        except Exception as e:
            logger.error(f"Error in nearest neighbor search: {str(e)}")
            raise FaceMatchingError(
                message="Nearest neighbor search failed",
                details=str(e)
            )

    @staticmethod
    def validate_match_threshold(distance: float, threshold: Optional[float] = None) -> bool:
        """
        Validate if a distance is within acceptable threshold.
        
        Args:
            distance: Euclidean distance to validate
            threshold: Threshold value (uses default if None)
            
        Returns:
            bool: True if within threshold, False otherwise
        """
        if threshold is None:
            threshold = FACE_MATCH_THRESHOLD
        
        is_valid = distance <= threshold
        logger.debug(f"Threshold validation: {distance:.4f} <= {threshold} = {is_valid}")
        return is_valid

    @staticmethod
    def batch_calculate_distances(
        query_embedding: List[float],
        database_embeddings: List[Tuple[int, List[float]]]
    ) -> List[Tuple[int, float]]:
        """
        Calculate distances from query to all database embeddings.
        
        Useful for analysis and debugging. Returns sorted by distance.
        
        Args:
            query_embedding: Query face embedding
            database_embeddings: List of (user_id, embedding) tuples
            
        Returns:
            List of (user_id, distance) sorted by distance (ascending)
        """
        try:
            distances = []
            
            for user_id, db_embedding in database_embeddings:
                try:
                    distance = FaceMatchingService.calculate_euclidean_distance(
                        query_embedding,
                        db_embedding
                    )
                    distances.append((user_id, distance))
                except FaceMatchingError:
                    logger.warning(f"Skipping invalid embedding for user {user_id}")
                    continue
            
            # Sort by distance (ascending)
            distances.sort(key=lambda x: x[1])
            return distances
            
        except Exception as e:
            logger.error(f"Error in batch distance calculation: {str(e)}")
            raise FaceMatchingError(
                message="Batch distance calculation failed",
                details=str(e)
            )

    @staticmethod
    def get_match_confidence(distance: float, threshold: Optional[float] = None) -> float:
        """
        Calculate confidence score for a match (0 to 1).
        
        Lower distance = higher confidence.
        Formula: confidence = (1 - (distance / threshold)) * 100, clamped to [0, 1]
        
        Args:
            distance: Euclidean distance
            threshold: Threshold value
            
        Returns:
            float: Confidence score from 0.0 to 1.0
        """
        if threshold is None:
            threshold = FACE_MATCH_THRESHOLD
        
        # Prevent division by zero
        if threshold <= 0:
            return 0.0
        
        # Calculate confidence: higher is better
        confidence = 1.0 - (distance / threshold)
        # Clamp to [0, 1]
        confidence = max(0.0, min(1.0, confidence))
        
        return confidence
