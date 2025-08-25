import streamlit as st
import difflib

def side_by_side_compare(original, optimized):
    """
    Clean side-by-side comparison without scroll buttons
    """
    if original is None or optimized is None:
        st.warning("Please optimize your resume first before comparing")
        return
    
    # CSS to make the text areas wider and taller
    st.markdown("""
    <style>
    .wide-textarea {
        width: 100% !important;
        height: 500px !important;
        font-family: monospace;
        font-size: 14px;
        line-height: 1.4;
    }
    .removed {
        background-color: #ffebee;
        color: #d32f2f;
        padding: 2px 4px;
        border-radius: 3px;
        text-decoration: line-through;
    }
    .added {
        background-color: #e8f5e8;
        color: #388e3c;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.subheader("📊 Side-by-Side Resume Comparison")
    
    # Create two columns for side-by-side view
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Original Resume")
        st.text_area(
            "Original Resume", 
            value=original, 
            height=500,  # Taller
            key="original_resume",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("### 🚀 Optimized Resume")
        st.text_area(
            "Optimized Resume", 
            value=optimized, 
            height=500,  # Taller
            key="optimized_resume", 
            label_visibility="collapsed"
        )
    
    # Now show the detailed differences
    st.markdown("---")
    st.subheader("🎯 Detailed Changes")
    
    d = difflib.Differ()
    diff = list(d.compare(original.splitlines(), optimized.splitlines()))
    
    changes_found = False
    
    # Create expandable sections for different types of changes
    removed_expander = st.expander("❌ Removed Content", expanded=True)
    with removed_expander:
        removed_lines = [line[2:] for line in diff if line.startswith('- ')]
        if removed_lines:
            for line in removed_lines:
                if line.strip():  # Only show non-empty lines
                    st.markdown(f"<div class='removed'>{line}</div>", unsafe_allow_html=True)
                    changes_found = True
        else:
            st.info("No content was removed")
    
    added_expander = st.expander("✅ Added Content", expanded=True)
    with added_expander:
        added_lines = [line[2:] for line in diff if line.startswith('+ ')]
        if added_lines:
            for line in added_lines:
                if line.strip():  # Only show non-empty lines
                    st.markdown(f"<div class='added'>{line}</div>", unsafe_allow_html=True)
                    changes_found = True
        else:
            st.info("No content was added")
    
    # Show summary
    st.markdown("---")
    st.subheader("📈 Change Summary")
    
    if changes_found:
        st.success(f"✅ Found {len(removed_lines)} removed lines and {len(added_lines)} added lines")
    else:
        st.info("No significant changes detected between the resumes")
        
    # Add download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Download Original",
            data=original,
            file_name="original_resume.txt",
            mime="text/plain"
        )
    
    with col2:
        st.download_button(
            label="📥 Download Optimized",
            data=optimized,
            file_name="optimized_resume.txt",
            mime="text/plain"
        )
