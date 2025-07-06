import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import gaussian_kde
import os

class AnalyzeResults():
    """
    AnalyzeResults:
        This class contains functions to:
        - estimate best paramaters values using posterior samples
        - 
    """  
    def __init__(
        self,
        overlap_analyzer_config,
        logger,
        **kwargs
    ):
        
        self.overlap_analyzer_config = overlap_analyzer_config
        self.logger = logger
        self.__dict__.update(kwargs)
        
        # For now hardcode the result path in ini file
        # result_path = self.overlap_analyzer_config.bns_parameter_estimation_configs.dingo_configs.result_dir
        # self.result = Result(file_name=result_path)
        # self.samples = pd.DataFrame(self.result.samples)
        self.summary = {}

    def perform_overlap_analysis(self, samples_dingo, dingo_weights, samples_fed, output_path):
        
        # === Updated plot function with 95% contours ===
        def plot_filled_kde(samples_list, names, colors, linestyles, title, meshgrid_number=50):
            samples_list = [np.array(s) for s in samples_list]
            all_theta = np.concatenate([s[:, 0] for s in samples_list])
            all_dl = np.concatenate([s[:, 1] for s in samples_list])

            # xmin, xmax = np.percentile(all_theta, [1, 99])
            # ymin, ymax = np.percentile(all_dl, [1, 99])

            # Solving Dingo plot being cut out
            # Use full range from data, not percentiles
            xmin, xmax = all_theta.min(), all_theta.max()
            ymin, ymax = all_dl.min(), all_dl.max()

            # Add generous buffer (10% instead of 5%)
            # buffer_x = 0.05 * (xmax - xmin)
            # buffer_y = 0.05 * (ymax - ymin)
            # xlim = (xmin - buffer_x, xmax + buffer_x)
            # ylim = (ymin - buffer_y, ymax + buffer_y)


            xx, yy = np.meshgrid(np.linspace(xmin, xmax, meshgrid_number), np.linspace(ymin, ymax, meshgrid_number))
            pos = np.vstack([xx.ravel(), yy.ravel()])

            fig, ax = plt.subplots(figsize=(5, 4))
            
            for s, name, color, ls in zip(samples_list, names, colors, linestyles):
                kde = gaussian_kde(s.T)
                zz = kde(pos).reshape(xx.shape)

                # Get 68% and 95% KDE levels
                z_sorted = np.sort(zz.ravel())[::-1]
                cumulative = np.cumsum(z_sorted)
                cumulative /= cumulative[-1]
                level_68 = z_sorted[np.searchsorted(cumulative, 0.68)]
                level_95 = z_sorted[np.searchsorted(cumulative, 0.95)]

                # Fill 68% region
                ax.contourf(
                    xx, yy, zz,
                    levels=[level_68, zz.max()],
                    colors=[color],
                    alpha=0.3,
                    antialiased=True
                )

                # 68% solid outline
                ax.contour(
                    xx, yy, zz,
                    levels=[level_68],
                    colors=[color],
                    linewidths=1.5,
                    linestyles=ls,
                    alpha=0.9,
                    label=f"{name} 68%"
                )

                # 95% dashed outline in same color
                ax.contour(
                    xx, yy, zz,
                    levels=[level_95],
                    colors=[color],
                    linewidths=1.2,
                    linestyles='dashed',
                    alpha=0.9,
                    label=None  # Avoid legend duplication
                )

            # Axis labels and title
            ax.set_xlabel(r"$\theta_{\rm obs}$ (rad)")
            ax.set_ylabel(r"$D_L$ (Mpc)")
            # ax.set_title(title)

            # ax.set_xlim(xlim)
            # ax.set_ylim(ylim)


            # Legend only shows 68% for each label
            legend_lines = [
                Line2D([0], [0], color=color, lw=2, linestyle=ls, label=f"{name}")
                for name, color, ls in zip(names, colors, linestyles)
            ]
            ax.legend(handles=legend_lines, loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=1)

            plt.tight_layout()
            plt.subplots_adjust(bottom=0.2)
            # plt.show()
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            fig.savefig(output_path)
            print(f" Saved corner plot: {output_path}")
            self.logger.info(f"Saved overlap contour plot: {output_path}")
            plt.close()


        # === Call updated plot ===
        plot_filled_kde(
            samples_list=[samples_dingo, samples_fed],
            names=['GW data (Dingo)', 'Radio data - federated fitting (afterglowpy)'],
            colors=['goldenrod', 'purple'],
            linestyles=['-', '-'],
            title='All data'
        )
    