from networkSecurity.exceptionHandling.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.artifactEntity import ClassificationMetricArtifact
from sklearn.metrics import precision_score, recall_score, f1_score

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        classification_metric_artifact = ClassificationMetricArtifact(
            precision_score=precision,
            recall_score=recall,
            f1_score=f1
        )

        logging.info(f"Classification Metric Artifact: {classification_metric_artifact}")

        return classification_metric_artifact

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e