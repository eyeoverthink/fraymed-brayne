"""
Test Suite for AGI Bootstrap Pre-Verse Engine
Tests specialized kernels for domain expertise.
"""

import pytest
from pre_verse_engine import (
    KernelResult, KernelBase, LanguageKernel, VisionKernel,
    ReasoningKernel, MemoryKernel, PreVerseEngine
)


# =============================================================================
# KERNEL BASE TESTS
# =============================================================================

class TestKernelResult:
    """Test KernelResult class."""
    
    def test_initialization(self):
        result = KernelResult(
            success=True,
            data={"key": "value"},
            confidence=0.9,
            processing_time=0.1,
            kernel_id="test_kernel"
        )
        assert result.success == True
        assert result.confidence == 0.9


class TestKernelBase:
    """Test KernelBase class."""
    
    def test_initialization(self):
        kernel = KernelBase("test_kernel", "cortex")
        assert kernel.kernel_id == "test_kernel"
        assert kernel.region == "cortex"
    
    def test_process_not_implemented(self):
        kernel = KernelBase("test_kernel", "cortex")
        result = kernel.process({"input": "test"})
        assert result.success == False


# =============================================================================
# LANGUAGE KERNEL TESTS
# =============================================================================

class TestLanguageKernel:
    """Test LanguageKernel class."""
    
    def test_initialization(self):
        kernel = LanguageKernel()
        assert kernel.kernel_id == "language_kernel"
        assert len(kernel.vocabulary) > 0
    
    def test_process_text(self):
        kernel = LanguageKernel()
        input_data = {"type": "text", "text": "the quick brown fox"}
        result = kernel.process(input_data)
        assert result.success == True
        assert "word_count" in result.data
        assert result.data["word_count"] == 4
    
    def test_vocabulary_coverage(self):
        kernel = LanguageKernel()
        input_data = {"type": "text", "text": "the and is"}
        result = kernel.process(input_data)
        assert result.confidence == 1.0  # All words in vocabulary


# =============================================================================
# VISION KERNEL TESTS
# =============================================================================

class TestVisionKernel:
    """Test VisionKernel class."""
    
    def test_initialization(self):
        kernel = VisionKernel()
        assert kernel.kernel_id == "vision_kernel"
        assert len(kernel.feature_detectors) > 0
    
    def test_process_image(self):
        kernel = VisionKernel()
        input_data = {
            "type": "image",
            "image_data": {
                "edges": ["e1", "e2"],
                "colors": ["red"],
                "shapes": ["circle"],
                "brightness": 0.5,
                "contrast": 0.5
            }
        }
        result = kernel.process(input_data)
        assert result.success == True
        assert "detected_edges" in result.data
        assert result.data["detected_edges"] == 2


# =============================================================================
# REASONING KERNEL TESTS
# =============================================================================

class TestReasoningKernel:
    """Test ReasoningKernel class."""
    
    def test_initialization(self):
        kernel = ReasoningKernel()
        assert kernel.kernel_id == "reasoning_kernel"
        assert len(kernel.rules) > 0
    
    def test_process_reasoning(self):
        kernel = ReasoningKernel()
        input_data = {
            "type": "logic",
            "premises": ["If it rains then the ground gets wet"],
            "query": "test"
        }
        result = kernel.process(input_data)
        assert result.success == True
        assert "inferences" in result.data
    
    def test_no_inferences(self):
        kernel = ReasoningKernel()
        input_data = {
            "type": "logic",
            "premises": ["This is a random statement"],
            "query": "test"
        }
        result = kernel.process(input_data)
        assert result.success == True
        assert result.data["inference_count"] == 0


# =============================================================================
# MEMORY KERNEL TESTS
# =============================================================================

class TestMemoryKernel:
    """Test MemoryKernel class."""
    
    def test_initialization(self):
        kernel = MemoryKernel()
        assert kernel.kernel_id == "memory_kernel"
        assert len(kernel.memory_store) == 0
    
    def test_store_and_retrieve(self):
        kernel = MemoryKernel()
        
        # Store
        store_result = kernel.process({
            "operation": "store",
            "key": "test_key",
            "value": "test_value"
        })
        assert store_result.success == True
        
        # Retrieve
        retrieve_result = kernel.process({
            "operation": "retrieve",
            "key": "test_key"
        })
        assert retrieve_result.success == True
        assert retrieve_result.data["value"] == "test_value"
    
    def test_retrieve_nonexistent(self):
        kernel = MemoryKernel()
        result = kernel.process({
            "operation": "retrieve",
            "key": "nonexistent_key"
        })
        assert result.success == True
        assert result.data["found"] == False


# =============================================================================
# PRE-VERSE ENGINE TESTS
# =============================================================================

class TestPreVerseEngine:
    """Test PreVerseEngine class."""
    
    def test_initialization(self):
        engine = PreVerseEngine()
        assert len(engine.kernels) == 4
        assert "language" in engine.kernels
        assert "vision" in engine.kernels
    
    def test_route_to_kernel(self):
        engine = PreVerseEngine()
        kernel_id = engine.route_to_kernel({"type": "text"})
        assert kernel_id == "language"
        
        kernel_id = engine.route_to_kernel({"type": "image"})
        assert kernel_id == "vision"
    
    def test_process_text(self):
        engine = PreVerseEngine()
        result = engine.process({"type": "text", "text": "test"})
        assert result["success"] == True
        assert result["kernel_id"] == "language_kernel"
    
    def test_process_multi_kernel(self):
        engine = PreVerseEngine()
        results = engine.process_multi_kernel(
            {"type": "text", "text": "test"},
            ["language", "reasoning"]
        )
        assert len(results) == 2
        assert all(r["success"] for r in results)
    
    def test_get_engine_statistics(self):
        engine = PreVerseEngine()
        stats = engine.get_engine_statistics()
        assert "total_kernels" in stats
        assert stats["total_kernels"] == 4
        assert "kernel_statistics" in stats


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
